function initTypewriterWordsAnimation(typewriterEl, words) {
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let isPaused = false;

    const typeSpeed = 80;
    const deleteSpeed = 50;
    const pauseAfterWord = 2000;
    const pauseBeforeDelete = 1500;

    function type() {
        const currentWord = words[wordIndex];

        if (isPaused) {
            return;
        }

        if (isDeleting) {
            typewriterEl.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;

            if (charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                setTimeout(type, 400);
                return;
            }
        } else {
            typewriterEl.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;

            if (charIndex === currentWord.length) {
                isPaused = true;
                setTimeout(() => {
                    isPaused = false;
                    isDeleting = true;
                    type();
                }, pauseBeforeDelete);
                return;
            }
        }

        const speed = isDeleting ? deleteSpeed : typeSpeed;
        setTimeout(type, speed);
    }

    // Start typewriter
    type();
}
