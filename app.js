const request = require("request")
const createError = require('http-errors')
const express = require('express')
const cookieParser = require('cookie-parser')
const logger = require('morgan')
const fs = require("fs")
const cors = require("cors")
const admzip = require("adm-zip")

var app = express()

var currentResults = []

app.use(cors())

app.use(logger('dev'))
app.use(express.json())
app.use(express.urlencoded({
  extended: false
}))
app.use(cookieParser())
app.get("/", (req, res) => {
  res.write("Boom!! It is GTU-ZILLA-API GO TO xxxxxxxxxxxxxxxxx")
  res.end()
})
fs.readFile("./papers.json", (error, data) => {
  if (!error) {
    papers = JSON.parse(data.toString())
  }
})
app.get("/pdf/*", (req, res) => {
  if (currentResults.includes(req.query.url)) {
    console.log("GOT a Request to Conver .zip to .pdf", req.query.url)
    request(req.query.url, {
      encoding: null
    }, (error, response, body) => {
      if (!response.headers['content-type'].startsWith("text/html") && !error) {
        console.log("recieved Body of ", req.query.url, "now trying to extract zip.")
        res.write(new admzip(body).getEntries()[0].getData())
        res.end()
      } else {

        res.status(504)
        res.write("Some Internal Error Occured..!!")
        res.end();
      }

    })
  } else {
    res.status(500)
    res.write("Some Internal Error Occured..!!")
    res.end()
  }

})

app.get("/papers/:code", (req, res) => {
  console.log(req.params, req.query)
  let code = req.params.code
  returnPapers(code).then(data => {
    result = data
    console.log(currentResults)
    res.json(result)
  })
})

async function returnPapers(code) {
  list = []
  papers.forEach(paper => {
    if (paper[0] == code) {
      currentResults.push(paper[1])
      list.push(paper)
    }
  })
  return list
}

app.use(function (req, res, next) {
  next(createError(404))
})
module.exports = app