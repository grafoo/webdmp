package main

import (
	"html/template"
	"log"
	"net/http"
)

func indexHandler(w http.ResponseWriter, r *http.Request) {
	t, err := template.ParseFiles("templates/index.html", "templates/head.html", "templates/login.html")

	if err != nil {
		log.Fatal(err)
	}

	t.ExecuteTemplate(w, "index", nil)
}

func faviconHandler(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "static/favicon.ico")
}

func main() {
	http.HandleFunc("/", indexHandler)

	http.HandleFunc("/favicon.ico", faviconHandler)

	staticHandler := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", staticHandler))

	http.ListenAndServe(":9090", nil)
}
