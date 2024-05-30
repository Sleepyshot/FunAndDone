  const openModalBtn = document.getElementById('openAddPlayer');
  const playerModal = document.getElementById('addPlayerModal');
  const closeButton = document.querySelector('.closePlayerModal');

  function openModal() {
      playerModal.style.display = 'block';
      playerModal.classList.add('slide-in');
  }

  function closeModal() {
      playerModal.classList.remove('slide-in');
      playerModal.style.display = 'none';
  }

  openModalBtn.addEventListener('click', openModal);
  closeButton.addEventListener('click', closeModal);

  const openColorBtn = document.getElementById('openColor');
  const dropdownColor = document.querySelector('.dropdownColor');
  
    function dropDownColor() { 
        if (dropdownColor.style.display === 'block')
            dropdownColor.style.display = 'none';
        else
            dropdownColor.style.display = 'block';
    }
  
    openColorBtn.addEventListener('click', dropDownColor);

    const openAvatarbtn = document.getElementById("openAvatar");
    const dropdownAvatar = document.querySelector(".dropdownAvatar")

        function dropDownAvatar() {
            if(dropdownAvatar.style.display === 'block')
                dropdownAvatar.style.display = 'none';

            else
            dropdownAvatar.style.display = 'block';
        }
    openAvatarbtn.addEventListener('click', dropDownAvatar);