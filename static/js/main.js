// Typing Effect
const roles = ["Backend Developer", "Python Developer", "Flask Developer"];
let index = 0;
let charIndex = 0;

function typeEffect() {
    const typingElement = document.getElementById("typing");
    if (!typingElement) return;

    if (charIndex < roles[index].length) {
        typingElement.innerHTML += roles[index].charAt(charIndex);
        charIndex++;
        setTimeout(typeEffect, 100);
    } else {
        setTimeout(() => eraseEffect(), 1500);
    }
}

function eraseEffect() {
    const typingElement = document.getElementById("typing");
    if (!typingElement) return;

    if (charIndex > 0) {
        typingElement.innerHTML = roles[index].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(eraseEffect, 50);
    } else {
        index = (index + 1) % roles.length;
        setTimeout(typeEffect, 300);
    }
}

typeEffect();


// ---------------------------
// Navbar Toggle
// ---------------------------
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav-links");

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("show");
});


// ---------------------------
// GSAP Stagger Animation (SAFE)
// ---------------------------
gsap.from(".project-card", {
    duration: 0.9,
    y: 30,
    opacity: 0,
    stagger: 0.15,
    ease: "power2.out"
});

// ---------------------------
// SAFE Floating Animation (FIXED)
// ---------------------------
gsap.to(".project-card", {
    y: -5,
    duration: 2.2,
    repeat: -1,
    yoyo: true,
    ease: "power1.inOut"
});
// ↑ Floating is now light (NOT removing cards from view)


// ---------------------------
// Tilt Effect (SAFE SETTINGS)
// ---------------------------
VanillaTilt.init(document.querySelectorAll(".project-card"), {
    max: 8,          // reduced tilt (fix clipping)
    speed: 300,
    glare: true,
    "max-glare": 0.2,
});

// GSAP - About Section Animations
if (document.querySelector(".about-section")) {
    gsap.from(".about-title", { duration: 1, y: 30, opacity: 0 });
    gsap.from(".about-text", { duration: 1, y: 40, opacity: 0, delay: 0.2, stagger: 0.2 });
    gsap.from(".skills-title", { duration: 1, y: 30, opacity: 0, delay: 0.5 });
    gsap.from(".about-skills span", { duration: 0.8, scale: 0.5, opacity: 0, stagger: 0.1, delay: 0.8 });
}

// GSAP Contact Page Animations
if (document.querySelector(".contact-section")) {

    gsap.from(".contact-title", {
        duration: 1,
        y: -20,
        opacity: 0,
        ease: "power2.out"
    });

    gsap.from(".contact-subtitle", {
        duration: 1,
        y: -15,
        opacity: 0,
        delay: 0.2,
        ease: "power2.out"
    });

    gsap.from(".contact-container", {
        duration: 1,
        scale: 0.8,
        opacity: 0,
        delay: 0.4,
        ease: "back.out(1.7)"
    });
}

// GSAP Resume Page Animations
if (document.querySelector(".resume-section")) {

    gsap.from(".resume-title", {
        duration: 1,
        y: -20,
        opacity: 0,
        ease: "power2.out"
    });

    gsap.from(".resume-subtitle", {
        duration: 1,
        y: -15,
        opacity: 0,
        delay: 0.2,
        ease: "power2.out"
    });

    gsap.from(".resume-card", {
        duration: 1,
        scale: 0.7,
        opacity: 0,
        delay: 0.4,
        ease: "back.out(1.4)"
    });
}

// Footer Animation
if (document.querySelector(".footer")) {
    gsap.from(".footer-title", { duration: 1, y: 20, opacity: 0 });
    gsap.from(".footer-text", { duration: 1, y: 20, opacity: 0, delay: 0.2 });
    gsap.from(".footer-social a", { duration: 0.6, scale: 0.5, opacity: 0, stagger: 0.15, delay: 0.4 });
    gsap.from(".footer-copy", { duration: 1, y: 20, opacity: 0, delay: 0.6 });
}
