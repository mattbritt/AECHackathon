// Puck.js samples & experiments
// includes two separate capabilities
// 1. toggle LED blink with button press
// 2. advertise batt and temp every 6 seconds
//   => DISCONNECT Puck from Web IDE to start advertising battery and temp


// Initial exercise to turn LED blink on and off with each button press
var LedOn = false;

function blinkParams (whichLED, durationMS){
  var howLong = durationMS ? durationMS : 5; 

  if (whichLED) {
    switch (whichLED) {
      case "r":
        LED1.write(true);
        setTimeout(function(){
          LED1.write(false);
        },howLong); 
        break;
      case "g":
        LED2.write(true);
        setTimeout(function(){
          LED2.write(false);
        },howLong); 
        break;
      case "b":
        LED3.write(true);
        setTimeout(function(){
          LED3.write(false);
        },howLong); 
        break;
      default:
        blinkNow();
      break;      
    }
  } else {
    blinkNow();
  }
}



var blinkId = setInterval(function() {
 // LedOn = !LedOn;
 // LED1.write(LedOn);
    blinkNow();
  }, 500);

function blinkNow (){
  LED1.write(true);
	setTimeout(function(){
		LED1.write(false);
	},5);
}

function startBlink(){
  blinkId = setInterval(function() {
	  blinkNow();
  }, 500);
}

function stopBlink (){
  LED1.write(false);
  clearInterval(blinkId);
}

stopBlink();

var blinkMode = false;

function toggle(){
  blinkMode = !blinkMode;
  if (blinkMode){
    startBlink();
  }else{
    stopBlink();
		console.log("temperature: ", E.getTemperature());
    console.log("battery level: ", Puck.getBatteryPercentage());
		console.log("light level: ", Puck.light());
  }
  console.log(“blinkMode is now ”, blinkMode);
}

setWatch(function(){toggle();},BTN, {edge:”rising”, debounce:50, repeat:true});

// for Pixl.js / Puck.js weather monitoring demo
//   http://www.espruino.com/Pixl.js+Wireless+Temperature+Display
// advertise battery and temperature every 6 seconds
//  DISCONNECT Puck from Web IDE to start advertising battery and temp

// increased temp resolution per:
//   http://forum.espruino.com/conversations/321891/#comment14275156
//   http://www.espruino.com/Reference#l_DataView_getUint8
//   https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView

var data = new Uint8Array(3); // 3 bytes
var d = new DataView(data.buffer);

function updateBT() {
    d.setUint8(0, Puck.getBatteryPercentage());
    d.setInt16(1, E.getTemperature()*256);
    NRF.setAdvertising({}, {
    manufacturer: 0x590,
    manufacturerData: data
  });
}

setInterval(updateBT, 6000);
updateBT();
