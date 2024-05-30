// start SITE GUIDANCE
    const guidanceModal = document.getElementById("siteGuidance");
    const closeGuidanceBtn = document.querySelector(".closeGuidance");
    const openGuidance = document.getElementById("openGuidance");

    function openGuidanceModal() {
        guidanceModal.style.display = "block";
        guidanceModal.classList.add("slide-in");
    }

    function closeGuidanceModal() {
        guidanceModal.style.display = "none";
        guidanceModal.classList.add("slide-in");
    }

    closeGuidanceBtn.addEventListener("click", closeGuidanceModal);
    openGuidance.addEventListener("click", openGuidanceModal);

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