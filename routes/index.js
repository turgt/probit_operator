const express = require('express');
const router = express.Router();
const { exec } = require("child_process");
const { execFile } = require("child_process");
const schedule   = require('node-schedule');
const mailer = require('nodemailer');
const moment = require('moment');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express',saat: moment(Date.now()).toDate() });
});

router.post('/', function(req, res, next) {
  execFile("/usr/bin/python3", ["main2.py", req.body.API_KEY,
      req.body.SECRET_KEY ,
      req.body.USDT ,
      req.body.rate ,
      req.body.multipler ,
      req.body.wait ,
      req.body.symbol]
      , (error, stdout, stderr) => {
    if (error) {
      console.log(`stdout: ${stdout}`);
      console.log(`error: ${error.message}`);
      res.send(`error: ${error.message}`);
      return;
    }
    if (stderr) {
      console.log(`stderr: ${stderr}`);
      res.send(`stderr: ${stderr}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    res.send(`stdout: ${stdout}`);
  });
  // res.send(req.body);
});
module.exports = router;
