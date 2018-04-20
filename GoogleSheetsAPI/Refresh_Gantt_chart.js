function Refresh() {
  // Select current sheet
  var ss = SpreadsheetApp.getActiveSheet();
  
  // Get value from a particular cell
  //var data = ss.getRange(2,1).getValue();
  var data = ss.getDataRange().getValues();
  var depval = 1;
  
  // Update the Start dates based upon their dependency
  for(i=1; i<16; i++) {
    if(data[i][4] != 0) {
//      msgBox("iteration",i)
//      msgBox("dependency", data[i][4])
      depval = data[i][4];
      newdate = ss.getRange(depval+1,7).getValue();        // getrange is not zero indexed, but 1 indexed
//      msgBox("value", newdate)
      ss.getRange(i+1,6).setValue(newdate);                // getrange is not zero indexed, but 1 indexed
      
    }
  }
  SpreadsheetApp.getActiveSheet().getRange('A19').setValue(data[0][0]);
}
  
  
function msgBox(message, message2) {
  // Creates a message box for debugging
  var ui = SpreadsheetApp.getUi(); // Same variations.

  var result = ui.alert(message, message2, 
      ui.ButtonSet.OK);

}
