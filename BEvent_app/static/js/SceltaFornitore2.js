  //Gestione dello scorrimento degli elementi all'interno di SceltaFornitore con aggiunta o rimozione di "in-page"
   // elements
   let elements_to_watch = document.querySelectorAll('.watch');

   // callback
   let callback = function(items){
     items.forEach((item) => {
       if(item.isIntersecting){
         item.target.classList.add("in-page");
       } else{
         item.target.classList.remove("in-page");
       }
     });
   }

   // observer
   let observer = new IntersectionObserver(callback, { threshold: 0.3 } );

   // apply
   elements_to_watch.forEach((element) => {
     observer.observe(element);
   });
