const marche = document.querySelectorAll('input[type="checkbox"]');
const tipoMezzoSelect = document.getElementById('tipo_mezzo');
const newUsedSelect = document.getElementById('new_used');
const prezzoMinInput = document.getElementById('mezzo-prezzomin');
const prezzoMaxInput = document.getElementById('mezzo-prezzomax');

const kmMinInput = document.getElementById('mezzo-kmmin');
const kmMaxInput = document.getElementById('mezzo-kmmax');

tipoMezzoSelect.addEventListener('change', aggiornaRisMezzzi);
newUsedSelect.addEventListener('change', aggiornaRisMezzzi);
prezzoMinInput.addEventListener('input', aggiornaRisMezzzi);
prezzoMaxInput.addEventListener('input', aggiornaRisMezzzi);
kmMinInput.addEventListener('input', aggiornaRisMezzzi);
kmMaxInput.addEventListener('input', aggiornaRisMezzzi);

marche.forEach(checkbox => {
    checkbox.addEventListener('change', aggiornaRisMezzzi);
});

// Function to update the displayed results based on selected filters
function aggiornaRisMezzzi() {
    var marca = [];
    const filtri = { marca };
    
    marche.forEach(checkbox => {
        if (checkbox.checked) {
            filtri["marca"].push(checkbox.value);
        }
    });

    filtri["tipo_mezzo"] = tipoMezzoSelect.value;
    filtri["new_used"] = newUsedSelect.value;
    filtri["mezzo-prezzomin"] = prezzoMinInput.value;
    filtri["mezzo-prezzomax"] = prezzoMaxInput.value;
    filtri["kmmin"] = kmMinInput.value;
    filtri["kmmax"] = kmMaxInput.value;

    fetch(`/get_filtered_mezzi/?${new URLSearchParams(filtri)}`)
        //controllo network
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const risultatiFiltri = document.getElementById('risultati_filtri');
            const noRes = document.getElementById('mezzi-no-res');

            // controllo errore parsing json
            if (data.result_html !== undefined) {

                //controllo che siano effettivamente dei mezzi da mostrare
                if (data.result_html.trim() === '') {
                    risultatiFiltri.style.display = 'none';
                    noRes.style.display = 'block';
                } else {
                    risultatiFiltri.style.display = 'flex';
                    noRes.style.display = 'none';
                    risultatiFiltri.innerHTML = data.result_html;
                }
                risultatiFiltri.innerHTML = data.result_html;
            } else {
                console.error("HTML content is undefined in the response.");
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
        });
}


const tipoAccSelect = document.getElementById('tipo_acc');
const prezzoMinInputAcc = document.getElementById('acc-prezzomin');
const prezzoMaxInputAcc = document.getElementById('acc-prezzomax');

tipoAccSelect.addEventListener('change', aggiornaRisAcc);
prezzoMinInputAcc.addEventListener('input', aggiornaRisAcc);
prezzoMaxInputAcc.addEventListener('input', aggiornaRisAcc);

function aggiornaRisAcc() {
    const filtri = {};

    filtri["tipo_acc"] = tipoAccSelect.value;
    filtri["acc-prezzomin"] = prezzoMinInputAcc.value;
    filtri["acc-prezzomax"] = prezzoMaxInputAcc.value;

    fetch(`/get_filtered_acc/?${new URLSearchParams(filtri)}`)
        //controllo network
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const risultatiFiltri = document.getElementById('risultati_filtri_acc');
            const noRes = document.getElementById('mezzi-no-res');

            // controllo errore parsing json
            if (data.result_html !== undefined) {

                //controllo che siano effettivamente dei mezzi da mostrare
                if (data.result_html.trim() === '') {
                    risultatiFiltri.style.display = 'none';
                    noRes.style.display = 'block';
                } else {
                    risultatiFiltri.style.display = 'flex';
                    noRes.style.display = 'none';
                    risultatiFiltri.innerHTML = data.result_html;
                }
                risultatiFiltri.innerHTML = data.result_html;
            } else {
                console.error("HTML content is undefined in the response.");
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
        });
}