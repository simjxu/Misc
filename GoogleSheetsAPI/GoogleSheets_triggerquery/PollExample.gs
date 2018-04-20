function doGet() {
  return HtmlService.createHtmlOutputFromFile('PollTest');    // Specify the html file that it should open
}

function doPoll(){
    $.post('ajax/test.html', function(data) {
        alert(data);  // process results here
        setTimeout(doPoll,5000);
    });
}

function createTrigger() {
  ScriptApp.newTrigger('querySpreadsheet')
  .timeBased()
  .everyHours(8)
  .create()
}

function deleteTrigger() {
  // Loop over all triggers and delete them
  var allTriggers = ScriptApp.getProjectTriggers();
  
  for (var i = 0; i < allTriggers.length; i++) {
    ScriptApp.deleteTrigger(allTriggers[i]);
  }
}

function querySpreadsheet() {
  // Function checks the spreadsheet to see if there are any that are past due
  
  // Define the slack webhook
  var SLACK_WEBHOOK_POST_URL = "https://hooks.slack.com/services/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";
  
  // Grab the data from the vendor spreadsheet
  var sheet = SpreadsheetApp.openById('1VJhxUmJvvG8AXm1w2obOgy4QaTyo0sIV7B5R_nJBQ8Y').getSheetByName('Open Purchases');
  var lastrow = sheet.getLastRow();
  var data = sheet.getDataRange().getValues()
  
  var now = new Date().valueOf();                        // Get the current date
  var celldate = data[2][2].valueOf();                   // Check the date of cell
  var isReceived = 'blank'
  
  for(i=1; i<lastrow; i++) {
    celldate = data[i][3].valueOf();
    isReceived = data[i][4];
    if(celldate != '' && now > celldate && isReceived == ''){
      // Collect item supposed to have delivered
      var itemname = data[i][0];
      var deliverystring = itemname.concat(' has not yet been delivered.');
      // post to slack webhook
      var payload = {
        "text" : deliverystring // <-- required parameter 
      }
      sendtoSlack(SLACK_WEBHOOK_POST_URL, payload);
    }
  }

  return 0
  
}

function sendtoSlack(url, payload) {
  var options =  {
    "method" : "post",
    "contentType" : "application/json",
    "payload" : JSON.stringify(payload)
  };
  return UrlFetchApp.fetch(url, options)
}
  