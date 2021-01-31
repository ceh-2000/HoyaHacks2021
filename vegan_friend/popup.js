var slideIndex = 1;

showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);

}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

// A function to get the most updated images
async function getPlots() {
    let parsedResponse = await fetch('http://localhost:5000/plots', {method: 'GET'})
                         .then(response => response.json());
    document.getElementById("image_1").src = parsedResponse.url1;
    document.getElementById("image_2").src = parsedResponse.url2;
    document.getElementById("caption_3").innerHTML = "You saved: ~"+parsedResponse.money_saved;
    // return "Hello";
}

function showSlides(n) {

  document.getElementById("intro").src = "images/vf_resized_logo-640_x_478.jpg";
  document.getElementById("image_3").src = "images/money.png";

  // let image1 = document.getElementById("image_1");
  // let image2 = document.getElementById("image_2");
  // let caption3 = document.getElementById("caption_3");
  Promise.resolve(getPlots());

  // plots.then(value =>
  //   caption3.innerHTML = value.money_saved;
  //
  // );
  // plots.then(value =>
  //   alert(value.money_saved);
  //   // document.getElementById("image_1").src = value.urls[0];
  //   // document.getElementById("image_2").src = value.urls[1];
  //   // document.getElementById("caption_3").innerHTML = value.money_saved;
  // );
  // alert(value.url1);
  // image1.src = value.url1;
  // image2.src = value.url2;

  // fetch a different URL for each plot each time

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

let dot0 = document.getElementById('dot_0');
dot0.onclick = function() {
  currentSlide(1);
};

let dot1 = document.getElementById('dot_1');
dot1.onclick = function() {
  currentSlide(2);
};

let dot2 = document.getElementById('dot_2');
dot2.onclick = function() {
  currentSlide(3);
};

let dot3 = document.getElementById('dot_3');
dot3.onclick = function() {
  currentSlide(4);
};

let dot4 = document.getElementById('dot_4');
dot4.onclick = function() {
  currentSlide(5);
};
