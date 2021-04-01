const $showCupcakesBtn = $('#show-cupcakes');
const $addCupcakesForm = $('#add-cupcake');
const $cupcakesList = $('#cupcakes-list');
const BASE_URL = 'http://127.0.0.1:5000/';

$showCupcakesBtn.click(showAllCupcakes);
// $addCupcakesForm.submit(addCupcake);
$cupcakesList.on('click', '#delete', deleteCupcake);

/** handle form for getting cupcakes from server */

async function showAllCupcakes() {

    //get cupcakes from API
    const cupcakes = await axios.get(`${BASE_URL}api/cupcakes`);
   
    // Append each cupcake to the DOM
    const cupArr = cupcakes.data.cupcakes;
    cupArr.forEach(function(cupcake) {
        $cupcakesList.append(buildCupcake(cupcake))
    });

    //Remove button from DOM
    $showCupcakesBtn.remove();
}

/** function for building HTML markup for a cupcake */

function buildCupcake(cupcake) {
    return `<li class="list-group-item" data-id='${cupcake.id}'><h4>Cupcake ${cupcake.id}</h4>
        <br>flavor: ${cupcake.flavor}
        <br>size: ${cupcake.size}
        <br>rating: ${cupcake.rating}
        <br><img src="${cupcake.image}" width="100">
        <br><button id="delete" class="btn btn-danger btn-small m-2">Delete</button></li>`
}

/** handle form for adding new cupcakes */

// async function addCupcake(evt) {
//     // Prevent default form behavior so we can send the form data via axios to server
//     evt.preventDefault();

//     // Get form values
//     let flavor = $('#flavor').val();
//     let size = $('#size').val();
//     let rating = $('#rating').val();
//     let image = $('#image').val();

//     // Send new cupcake post request to server
//     const newCupCakeRes = await axios.post(`${BASE_URL}api/cupcakes`, {flavor, size, rating, image});

//     // Create new Cupcake from server response & append the Cupcake to the DOM list
//     let $newCupcake = $(buildCupcake(newCupCakeRes.data.cupcake));
//     $cupcakesList.append($newCupcake);

//     //clear form data
//     $addCupcakesForm.trigger('reset');
// }

/** handle form for deleting a cupcake */

async function deleteCupcake(evt) {
    evt.preventDefault();

    // get cupcake li element and cupcake id for event target
    let $cupcake = $(evt.target).closest("li");
    let cupcakeID = $cupcake.attr("data-id");

    //delete the cupcake from the DB
    await axios.delete(`${BASE_URL}/api/cupcakes/${cupcakeID}`);

    //remove the cupcake from the DOM
    $cupcake.remove();

    //reload window to display confirmation message
    location.reload();
}