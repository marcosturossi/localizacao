// Duplica Formulário

let formList = document.querySelectorAll("#form-container")
let addButton = document.querySelector("#add-form")
let removeButton = document.querySelector('#remove-form')
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")
let beforeForm = document.querySelector("#before_form")
let formNum = formList.length -1;
let newForm;

addButton.addEventListener('click', addForm)
removeButton.addEventListener('click', removeForm)

function addForm(e){
    // Cria um novo formulário, e gerência a quantidade de formulário no managemedform(django)
    e.preventDefault();
    let newForm = formList[0].cloneNode(true);
    let formRegex = RegExp('form-(\\d){1}-', 'g')

    formNum++;
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);
    beforeForm.appendChild(newForm);

    totalForms.setAttribute('value', `${formNum + 1}`);
    return newForm
}
function removeForm(e){
    // Remove o ultimo elemento adicionado na lista de formulários
    let formList = document.querySelectorAll("#form-container");
    let ultimo = formList[formList.length -1]
    if (formList.length > 1){
        ultimo.remove()
        totalForms.setAttribute('value', `${formNum - 1}`);
    }
}
