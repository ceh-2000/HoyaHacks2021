var slideIndex = 1;
document.getElementById("image_1").src = "https://s35930.p1154.sites.pressdns.com/wp-content/uploads/2019/10/vegan-plant-based-news-meme1.png";
document.getElementById("image_2").src = "https://www.totallyveganbuzz.com/wp-content/uploads/2018/11/25-Hilarious-vegan-memes-that-provide-valuable-emotional-support_TotallyVeganBuzz-1280x720.jpg";
document.getElementById("image_3").src = "https://static.boredpanda.com/blog/wp-content/uploads/2018/10/vegan-memes-fb32-png__700.jpg";
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

