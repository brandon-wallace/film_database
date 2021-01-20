console.log(`Javascript file enabled.`);

const deleteBtn = document.querySelectorAll('.data-item');


const deleteItem = (event) => {
    const endpoint = '/delete/${id}';
    console.log(endpoint);

    fetch(endpoint, { 
        method: 'DELETE'
    } 
        .then(() => {}) 
        .catch((err) => console.error(err.message))
    )
};


for (let i = 0; i < deleteBtn.length; i++) {
    deleteBtn[i].addEventListener('click', deleteItem);
};
