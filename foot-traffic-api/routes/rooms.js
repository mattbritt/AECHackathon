var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/:id?', function(req, res) {
  return res.send('This is fun!!!')
});

module.exports = router;
