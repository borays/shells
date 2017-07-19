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
	URL  string = "http://www.mzitu.com/mm"
	PATH string = "/mm"
)

var (
	c1 chan string
	c2 chan string
	c3 chan int
)

func init() {
	c1 = make(chan string, 100)  //url
	c2 = make(chan string, 1000) //image url
	c3 = make(chan int, 1000)

}

func getHtmlContent(url string) (content string) {
	// version 1
	//	response, err := http.Get(url)
	//	checkErr(err)

	//	defer response.Body.Close()
	//	str, err := ioutil.ReadAll(response.Body)
	//	checkErr(err)
	//	return string(str)

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

func regexpHtml() {
	fnum := 1
	reg, err := regexp.Compile(`<li><a href=\"(.*?)\" target=\"_blank\">`)
	checkErr(err)
	content := getHtmlContent(URL)
	list_1 := reg.FindAllStringSubmatch(content, 1000)
	for _, item_1 := range list_1 {
		c1 <- item_1[1]
		// fmt.Println(item[1])
	}
	close(c1)

	for info := range c1 {
		// fmt.Println(info)
		reg2, err := regexp.Compile(`<span>([0-9]{2})<\/span>`)
		checkErr(err)

		content_2 := getHtmlContent(info)
		list_2 := reg2.FindAllStringSubmatch(content_2, 100)

		for _, item_2 := range list_2 {
			// fmt.Println(item_2[1])
			page, _ := strconv.Atoi(item_2[1])
			for i := 1; i < page; i++ {
				url_2 := info + "/" + strconv.Itoa(i)
				reg3, err := regexp.Compile(`<img src=\"(.*?)\" alt=(.*?)>`)
				checkErr(err)
				content_3 := getHtmlContent(url_2)

				list_3 := reg3.FindAllStringSubmatch(content_3, 1000)

				for _, item_3 := range list_3 {
					//fmt.Println(item_3[1])

					//下载图片
					info, err := os.Stat(PATH)
					if err != nil || info.IsDir() == false {
						err := os.Mkdir(PATH, os.ModePerm)
						checkErr(err)
					}

					image_body := getImage(item_3[1])
					filename := PATH + "/" + strconv.Itoa(fnum) + ".jpg"
					ioutil.WriteFile(filename, image_body, 0644)
					fmt.Println("Downloading...", item_3[1])
					fnum++
				}

			}

		}
	}
}

func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	regexpHtml()

}
