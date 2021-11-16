const navSlide = () => {
    const burger = document.querySelector('.burger');
    const header = document.querySelector('.items-list');
    const itemLinks =  document.querySelectorAll('.items-list li');

    burger.addEventListener('click', ()=>{
        //Toggle Nav
        header.classList.toggle('item-active');

        //Animate Links
        itemLinks.forEach((link, index)=>{
            if(link.style.animation) {
                link.style.animation = ''
            } else {
                link.style.animation = `headerLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });
        //Burger animation
        burger.classList.toggle('toggle');
    });

}

navSlide();