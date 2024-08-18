const accordion = document.getElementsByClassName('container');

for (i=0; i<accordion.length; i++) {
  accordion[i].addEventListener('dblclick', function () {
    this.classList.toggle('active')
  })
}