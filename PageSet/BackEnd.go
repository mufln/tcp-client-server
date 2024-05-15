package main

import (
	"fmt"
	"html/template"
	"net/http"
)

// это не нужный код, но нужный чтобы я не забыла функции
func main() {

	fmt.Println("Server is listening...")

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "MainPage.html")
	})

	http.HandleFunc("/10", func(w http.ResponseWriter, r *http.Request) {
		data := "Button number two"
		tmpl, _ := template.New("data").Parse("<div class='name'>{{ .}}</div>")
		tmpl.Execute(w, data)
	})

	http.ListenAndServe(":8181", nil)

}
