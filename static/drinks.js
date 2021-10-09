/// Script for drinks.html template

// $drinksList = $('#drinks-list');
// $searchForm = $('form');
// $searchForm.on('submit', handleForm);
$nameField = $('#name');
$categoryField = $('#category');
$ingredientField = $('#ingredient')
$clearBtn = $('#clear-btn');

/// Clears SearchForm fields upon button click
$clearBtn.click(() => {
    $nameField.val('');
    $categoryField.val('0');
    $ingredientField.val('0');

    const resp = axios.post('/clear-search')
    // console.log(resp.data['STATUS'])
});

// /// Event Handler function for handling AJAX requests via Axios to the server, fetches drink data, and replaces drink list on DOM
// async function handleForm(evt) {

//     evt.preventDefault();

//     formData = $searchForm.serializeArray();

//     const resp = await axios.post(`/drinks?page=1`, formData);

//     drinkData = resp.data;

//     $drinksList.html('');

//     for (let drink of drinkData) {
//         $drinksList.append(
//             $('<tr>').attr('id', drink['id']).append([
//                 $('<td>').append(
//                     $('<img>').attr({
//                         'src': drink.image_url,
//                         'width': '200px',
//                         'class': 'mx-auto d-inline rounded img-thumbnail',
//                         'alt': ''
//                     })
//                 ),
//                 $('<td>').attr('class', 'align-middle').append(
//                     $('<a>').attr({
//                         'href': `/drinks/${drink['id']}`,
//                         'class': 'display-5 d-inline text-decoration-none text-wrap'
//                     }).text(drink['name'])
//                 ),
//                 $('<td>').attr('class', 'align-middle').append(
//                     $('<h1>').attr('class', 'd-inline text-right')
//                     .append(
//                         $('<span>').attr({
//                             'id': drink["category_id"],
//                             'class': 'tag-pill rounded-pill bg-primary text-light px-3',
//                         }).text(drink["category"])
//                     )
//                 )
//             ])
//         );
//     }
// }
