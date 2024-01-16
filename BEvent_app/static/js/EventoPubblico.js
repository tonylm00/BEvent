document.addEventListener('DOMContentLoaded', function() {

    var uploadButton = document.getElementById('upload-button');
    uploadButton.addEventListener('click', function() {
        var fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.onchange = e => {
           var file = e.target.files[0];
           var reader = new FileReader();
           reader.readAsDataURL(file);
           reader.onload = readerEvent => {
              var content = readerEvent.target.result;
              console.log('Image uploaded:', content);

           };
        }
        fileInput.click();
    });

    let ticketsAvailable = document.getElementById('tickets-available');
    ticketsAvailable.addEventListener('change', function() {
        console.log('Tickets available:', ticketsAvailable.value);

    });


    var supplierInput = document.getElementById('supplier');
    supplierInput.addEventListener('change', function() {
        console.log('Supplier:', supplierInput.value);

    });


    var eventTypeSelect = document.getElementById('event-type');
    eventTypeSelect.addEventListener('change', function() {
        console.log('Event type:', eventTypeSelect.value);

    });
});
