document.addEventListener('DOMContentLoaded', function () {

   function createStarRating(ratingId) {
    const container = document.getElementById(ratingId);
    for (let i = 5; i >= 1; i--) {
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.id = ratingId + '-star-' + i;
        radio.name = ratingId;
        radio.value = i;

        const label = document.createElement('label');
        label.htmlFor = ratingId + '-star-' + i;
        label.innerHTML = '&#9733;';

        container.appendChild(radio);
        container.appendChild(label);
    }
}

    function setRating(starContainer, rating) {
        Array.from(starContainer.children).forEach((star, index) => {
            star.style.color = index < rating ? '#ffd700' : '#ccc';
        });
    }

});
