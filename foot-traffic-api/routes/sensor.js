var express = require('express');
var router = express.Router();
const crypto = require('crypto');
const { database } = require('../app')
const secret = 'abcdefg';
var uuid = require('uuid4');

router.post('/:deviceID', function(req, res) {
  const data = req.body.DATA || req.body.data
  const deviceID = req.params.deviceID

      const rooms = req.db
        // .db('foot-traffic')
        .collection('rooms');

      rooms
        .findOne({id: deviceID}, (err, record) => {
          if (record) {
            if (data.toLowerCase() === "forward") {
              rooms.findOneAndUpdate(
                {id:record.roomID},
                {$inc: {count:1}},
                { returnOriginal: false},
                (err, doc) => {
                  if (err) {
                    return res.sendStatus(501)
                  }
                  return res.status(201).json({count: doc.value.count})
                }
              )
            } else {
              rooms.findOneAndUpdate(
                { id:record.roomID },
                { $inc: {count:-1} },
                { returnOriginal: false },
                (err, doc) => {
                  if (err) {
                    return res.sendStatus(501)
                  }
                  return res.status(201).json({count: doc.value.count})
                }
              )
            }
          } else {
            const id = uuid();

            rooms.insertOne({id:deviceID, roomID: id})
            if (data.toLowerCase() === "forward") {
              rooms.insertOne({id, count: 1}, (err, result) => {
                if (err) return res.sendStatus(501)
                const {count} = result.ops[0]
                return res.status(201).json({count})
              })
            } else {
              rooms.insertOne({id, count: 0}, (err, result) => {
                if (err) return res.sendStatus(501)
                const {count} = result.ops[0]
                return res.status(201).json({count})
              })
            }
          }
        })
  //   }
  // })


});

module.exports = router;
