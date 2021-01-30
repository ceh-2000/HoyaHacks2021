var slideIndex = 1;
document.getElementById("image_1").src = "https://storage.googleapis.com/hoyahacks2021.appspot.com/test.png";
document.getElementById("image_2").src = "https://storage.googleapis.com/hoyahacks2021.appspot.com/test.png";
document.getElementById("image_3").src = "https://storage.googleapis.com/hoyahacks2021.appspot.com/test.png";
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

let prevButton = document.getElementById('prev');
prevButton.onclick = function() {
  plusSlides(-1);
};

let nextButton = document.getElementById('next');
nextButton.onclick = function() {
  plusSlides(1);
};

let dot1 = document.getElementById('dot_1');
dot1.onclick = function() {
  currentSlide(1);
};

let dot2 = document.getElementById('dot_2');
dot2.onclick = function() {
  currentSlide(2);
};

let dot3 = document.getElementById('dot_3');
dot3.onclick = function() {
  currentSlide(3);
};

