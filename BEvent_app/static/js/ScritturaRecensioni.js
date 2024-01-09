document.addEventListener('DOMContentLoaded', function () {
    // Create stars for each rating type
    createStarRating('overall-rating');
    createStarRating('scenografia-rating');
    createStarRating('accoglienza-rating');
    createStarRating('professionalita-rating');

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

    document.getElementById('submit-review').addEventListener('click', function() {
        // Logic to handle the submission of the review
        const title = document.getElementById('review-title').value;
        const body = document.getElementById('review-body').value;
        const overallRating = getRatingValue('overall-rating');
        const hydrationRating = getRatingValue('scenografia-rating');
        const freshnessRating = getRatingValue('accoglienza-rating');
        const deepcleanRating = getRatingValue('professionalita-rating');

        console.log({
            title,
            body,
            ratings: {
                overall: overallRating,
                scenografia: scenografiaRating,
                accoglienza: accoglienzaRating,
                professionalita: professionalitaRating
            }
        });
    });
});
