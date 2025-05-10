document.addEventListener('DOMContentLoaded', function () {
    initParticles();

    let resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            // Full reset: remove and recreate #particles-js container
            const oldParticles = document.getElementById('particles-js');
            if (oldParticles) oldParticles.remove();

            const newParticles = document.createElement('div');
            newParticles.id = 'particles-js';
            newParticles.style.position = 'fixed';
            newParticles.style.top = '0';
            newParticles.style.left = '0';
            newParticles.style.width = '100vw';
            newParticles.style.height = '100vh';
            newParticles.style.zIndex = '0';
            newParticles.style.backgroundColor = '#0a0815';

            document.body.prepend(newParticles); // add it to the very top

            initParticles(); // fresh init
        }, 300);
    });
});

function initParticles() {
    particlesJS("particles-js", {
        particles: {
            number: {
                value: 100,
                density: {
                    enable: true,
                    value_area: 700
                }
            },
            color: { value: "#6d8cc4" },
            shape: {
                type: "circle",
                stroke: { width: 0, color: "#000000" }
            },
            opacity: {
                value: 0.9,
                random: true,
                anim: {
                    enable: true,
                    speed: 0.8,
                    opacity_min: 0.5,
                    sync: false
                }
            },
            size: {
                value: 4,
                random: true,
                anim: {
                    enable: true,
                    speed: 3,
                    size_min: 2,
                    sync: false
                }
            },
            line_linked: {
                enable: true,
                distance: 120,
                color: "#6d8cc4",
                opacity: 0.3,
                width: 1.2
            },
            move: {
                enable: true,
                speed: 3.5,
                direction: "none",
                random: true,
                straight: false,
                out_mode: "out",
                bounce: false,
                attract: {
                    enable: true,
                    rotateX: 800,
                    rotateY: 1600
                }
            }
        },
        interactivity: {
            detect_on: "canvas",
            events: {
                onhover: {
                    enable: true,
                    mode: "grab"
                },
                onclick: {
                    enable: true,
                    mode: "bubble"
                },
                resize: true
            },
            modes: {
                grab: {
                    distance: 130,
                    line_linked: {
                        opacity: 0.6
                    }
                },
                bubble: {
                    distance: 250,
                    size: 12,
                    duration: 0.3,
                    opacity: 0.8,
                    speed: 3
                }
            }
        },
        retina_detect: true
    });
}
