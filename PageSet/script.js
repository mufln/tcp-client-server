const tx = document.getElementsByTagName("textarea");
for (let i = 0; i < tx.length; i++) {
  tx[i].setAttribute("rows", tx[i].rows + 1);
  tx[i].addEventListener("input", OnInput, false);
  if (document.getElementsByClassName("text-field")[0].offsetHeight >= 150){
    break;
  }
}

function OnInput() {
    this.rows = this.rows;
}