$(function () {


  $('#submitBtn').on('click', function () {
      log('Hello World');
      var etudiantList = [];
      $('#etudiant-list tr').each(function () {
        $(this).find('td input:checked').each(function () {
          var checkedRow = $(this).closest('tr');
          etudiantList.push({
            'id': this.value,
            'matricule_etudiant': $(checkedRow).find('td:eq(1)').text(),
            'nom_etudiant': $(checkedRow).find('td:eq(2)').text(),
            'prenom_etudiant': $(checkedRow).find('td:eq(3)').text()

          });
        });
      });
      // check nothing selected
      // console.log(JSON.stringify(customerList));
      if (etudiantList.length) {
          console.log("Hello");
       $.ajax({
         type: "POST",
         url: "export/",  // the endpoint
         data: {question_data: JSON.stringify(etudiantList)},
         success: function(data) {
           $('#etudiant-form')[1].reset();
         },
         error : function(xhr,errmsg,err) {
           console.log("An error");
         }
        });
      }
      else{
        console.log('No items were entered')
      }
  });
});
