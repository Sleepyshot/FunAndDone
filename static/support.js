const openSubjectBtn = document.getElementById('openSubjectButton');
const dropdownSubject = document.querySelector('.dropdownSubject');

  function dropSubject() { 
      if (dropdownSubject.style.display === 'block')
          dropdownSubject.style.display = 'none';
      else
          dropdownSubject.style.display = 'block';
  }

  openSubjectBtn.addEventListener('click', dropSubject);


const openDescribeBtn = document.getElementById('openDescribeButton');
const dropdownDescribe = document.querySelector('.dropdownDescribe');

    function dropDescribe() { 
        if (dropdownDescribe.style.display === 'block')
            dropdownDescribe.style.display = 'none';
        else
            dropdownDescribe.style.display = 'block';
    }

openDescribeBtn.addEventListener('click', dropDescribe);