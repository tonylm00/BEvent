// Questo codice dovrebbe essere modificato per recuperare i dati delle recensioni effettive.
document.addEventListener('DOMContentLoaded', function() {
  // Qui dovremmo mettere il codice per caricare le recensioni dal server o da un database
  const reviews = recensioni

  const reviewsContainer = document.querySelector('.reviews-container');


  reviews.forEach(review => {
    const reviewElement = document.createElement('div');
    reviewElement.classList.add('review');
    reviewElement.innerHTML = `
      <div class="review-title">${review.title}</div>
      <div class="review-rating">${'★'.repeat(review.rating)}</div>
      <p class="review-body">${review.body}</p>
    `;
    reviewsContainer.appendChild(reviewElement);
  });
});
