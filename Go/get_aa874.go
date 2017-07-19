package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"

	"github.com/parnurzeal/gorequest"
)

const (
	PATH string = "/aa874"
)

var (
	c1 chan string
	c2 chan string
	c3 chan string
)

func init() {
	c1 = make(chan string, 1000) //page Url
	c2 = make(chan string, 1000) //tiezi Url
	c3 = make(chan string, 1000) //image url

}

func getHtmlContent(url string) (content string) {
	request := gorequest.New()
	_, body, _ := request.Get(url).
		Set("User-Agent", "Opera/9.80 (Windows NT 6.1; WOW64; U; de) Presto/2.10.289 Version/12.01").
		End()
	return string(body)
}

func getImage(url string) (image_body []byte) {
	request := gorequest.New()
	resq, _, _ := request.Get(url).
		Set("User-Agent", "Opera/9.80 (Windows NT 6.1; WOW64; U; de) Presto/2.10.289 Version/12.01").
		End()
	str, err := ioutil.ReadAll(resq.Body)
	checkErr(err)
	image_body = str
	return image_body

}

func get_page_info() {
	for i := 0; i <= 30; i++ {
		url_first := "https://aa874.com/htm/piclist9/" + strconv.Itoa(i) + ".htm"
		c1 <- url_first

	}
	close(c1)

}

func get_tiezi_url(c chan string) {
	reg, err := regexp.Compile(`<li><a href=\"(.*?)\" target=\"_blank\">`)
	checkErr(err)
	for page := range c {
		tiezi_content := getHtmlContent(page)
		tiezis := reg.FindAllStringSubmatch(tiezi_content, 1000)
		for _, tiezi_info := range tiezis {
			tiezi_url := "https://aa874.com" + tiezi_info[len(tiezi_info)-1]
			c2 <- tiezi_url
		}
	}
}

func get_tiezi_image(c chan string) {
	reg, err := regexp.Compile(`src=\"(.*?)\"><br>`)
	checkErr(err)
	for image_info := range c {
		images_content := getHtmlContent(image_info)
		images := reg.FindAllStringSubmatch(images_content, 1000)
		for _, image_info := range images {
			image_url := image_info[len(image_info)-1]
			c3 <- image_url
		}
	}
}

func Downloading(c chan string) {
	fnum := 1
	info, err := os.Stat(PATH)
	if err != nil || info.IsDir() == false {
		err := os.Mkdir(PATH, os.ModePerm)
		checkErr(err)
	}
	for image_url := range c {
		//		fmt.Println(image_url)
		image_body := getImage(image_url)
		filename := PATH + "/" + strconv.Itoa(fnum) + ".jpg"
		ioutil.WriteFile(filename, image_body, 0644)
		fmt.Println("Downloading..." + strconv.Itoa(fnum) + " Pics")
		fnum++
	}

}

func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	go get_page_info()
	get_tiezi_url(c1)
	go get_tiezi_image(c2)
	Downloading(c3)

}
