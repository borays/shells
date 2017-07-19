package main

import (
	"bufio"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	uri string = "https://github.com/trending?l="
)

var results chan string

func main() {
	var content string
	results = make(chan string, 10)
	var waitGroup sync.WaitGroup

	var languages = []string{"go", "python", "ruby", "java", "javascript", "c#", "bash"}
	waitGroup.Add(len(languages))
	filename := time.Now().Format("2006-01-02")

	for _, elem := range languages {

		go func(elem string) {
			url := uri + elem
			scrape(url, elem)
			waitGroup.Done()

		}(elem)

	}

	go func() {
		waitGroup.Wait()
		close(results)
	}()

	//	for info := range results {
	//		fmt.Print(info)
	//	}

	for a := 0; a < len(languages); a++ {
		content = content + <-results
	}
	content = "### " + filename + "\n" + content
	writeMD(filename, content)
	fmt.Println("程序执行完毕！")

}

func scrape(url, lang string) {
	var doc *goquery.Document
	var e error

	result := "\n" + lang + "\n"

	if doc, e = goquery.NewDocument(url); e != nil {
		fmt.Println("错误信息:", e.Error())
	}

	doc.Find("ol.repo-list li").Each(func(i int, s *goquery.Selection) {
		title := s.Find("h3 a").Text()
		description := s.Find("p.col-9").Text()
		url, _ := s.Find("h3 a").Attr("href")
		url = "https://github.com" + url
		var stars = "0"
		var forks = "0"
		s.Find("a.muted-link.mr-3").Each(func(i int, contentSelection *goquery.Selection) {
			if temp, ok := contentSelection.Find("svg").Attr("aria-label"); ok {
				switch temp {
				case "star":
					stars = contentSelection.Text()
				case "fork":
					forks = contentSelection.Text()
				}
			}
		})
		result = result + "*[" + strings.Replace(strings.TrimSpace(title), " ", "", -1) + " (" + strings.TrimSpace(stars) + "s/" + strings.TrimSpace(forks) + "f)](" + url + ") : " + strings.TrimSpace(description) + "\n"
	})
	fmt.Println(lang + " 分析完成！")
	results <- result
}

func writeMD(filename, content string) {
	fo, err := os.Create(filename + ".md")
	if err != nil {
		panic(err)
	}

	defer fo.Close()

	w := bufio.NewWriter(fo)
	w.WriteString(content)
	w.Flush()

}
