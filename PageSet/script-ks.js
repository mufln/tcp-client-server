////////это не работает как надо
var tx = document.getElementsByClassName('textarea');
for (var i = 0; i < tx.length; i++) {
  tx[i].setAttribute('style', 'height:' + (tx[i].scrollHeight) + 'px;overflow:auto;');
  tx[i].addEventListener("input", OnInput, false);
}

function OnInput(e) {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
}

//////////это тоже не работает

function setfilename(val)
  {
    var fileName = val.substr(val.lastIndexOf("\\")+1, val.length);
    document.getElementById("uploadFile").value = fileName;
  }
/////////////здесь мы автоматом крутим вниз
var scrollDiv = document.getElementById("messages");
scrollDiv.scrollTo(0, scrollDiv.scrollHeight);

/////////////здесь обработка сообщений
const form = document.getElementById("sender-form");

function handleForm(event) { 
  // $('#messages').load(document.URL + ' #messages');
  event.preventDefault();
  event.target.reset();
} 

form.addEventListener('submit', handleForm);


///////// крутим вниз по кнопке
function pageScroll() {
  const $messages = document.querySelector('#messages');
  $messages.scrollTop = $messages.scrollHeight;
}

//// увеличиваем высоту текстового поля
function auto_grow(element) {
  element.style.height = "5px";
  element.style.height = (element.scrollHeight)+"px";
}