// start OPEN delete MODAL
    const openModalBtn = document.getElementById('openDeleteAccount');
    const deleteModal = document.getElementById('deleteContent');
    const closeDeleteAccount = document.querySelector(".closeVerifyModal")

    function openDeleteModal() {
        deleteModal.style.display = 'block';
        deleteModal.classList.add('slide-in');
    }

    function closeDeleteModal() {
        deleteModal.style.display = 'none';
        deleteModal.classList.add('slide-in');
    }

    openModalBtn.addEventListener('click', openDeleteModal);
    closeDeleteAccount.addEventListener('click', closeDeleteModal);

    const deleteConfirmation = document.querySelector('.deleteConfirmation');
    deleteConfirmation.addEventListener('click', () =>{
        fetch("/deleteAccount", {//this is our route for querying the DELETE
            method: "POST",
        })
        .then(response => {
            if(response.ok)
            {
                // we handle all logic inside the app.py
                window.location.href = "/";// redirect to login
            }
            else
            {
                const errorModal = document.getElementById("errorContent");
                const closeErrorModal = document.querySelector(".closeErrorModal");

                errorModal.style.display = "block";
                deleteModal.style.display = "none";

                closeErrorModal.addEventListener('click', () => {
                    errorModal.style.display = "none";
                });
            }   
        })
        .catch(error =>{ 
            const errorModal = document.getElementById("errorContent");
            const closeErrorModal = document.querySelector(".closeErrorModal");

            errorModal.style.display = "block";

            closeErrorModal.addEventListener('click', () => {
            errorModal.style.display = "none";
            })
        });
    });


// start OPEN players MODAL
    const openPlayerBtn = document.getElementById('openDeletePlayers');
    const playerModal = document.getElementById('playerList');
    const closePlayerModal = document.querySelector(".closePlayerModal")

    function openPlayerModal() {
        playerModal.style.display = 'block';
        playerModal.classList.add('slide-in');
    }

    function closePlayer() {
        playerModal.style.display = 'none';
        playerModal.classList.add('slide-in');
    }

    openPlayerBtn.addEventListener('click', openPlayerModal);
    closePlayerModal.addEventListener('click', closePlayer);


// start BACK TO TOP
    const backToTopBtn = document.getElementById("backToTopBtn");

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () {
        scrollFunction();
    };

    function scrollFunction() {
        if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
            backToTopBtn.style.display = "block";
        } else {
            backToTopBtn.style.display = "none";
        }
    }
        
    // When the user clicks on the button, scroll to the top of the document
    backToTopBtn.addEventListener("click", function () {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
    });
