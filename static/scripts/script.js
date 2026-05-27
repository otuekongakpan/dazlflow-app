const moodMatrix = {
    vulnerable: {
        voice: "“You’re safe here. Let’s find something that holds you gently.”",
        tags: ["Reflective", "Soft Glow", "For the Dreamers"],
        bgTint: "rgba(24, 12, 36, 0.35)",
        chord: [110, 165, 220, 275], 
        type: 'sine'
    },
    numb: {
        voice: "“Static frequency detected. Injecting low-end analog heat to kickstart the pulse.”",
        tags: ["White Noise", "Sub-Bass", "Industrial"],
        bgTint: "rgba(16, 20, 28, 0.35)",
        chord: [55, 110, 146.83], 
        type: 'sawtooth'
    },
    confident: {
        voice: "“High output velocity. Matching your current rhythm with high-friction cadence.”",
        tags: ["Kinetic", "Heavy Syncopation", "Anthem"],
        bgTint: "rgba(0, 32, 50, 0.35)",
        chord: [146.83, 220, 293.66], 
        type: 'triangle'
    },
    focused: {
        voice: "“Isolating external noise. Calibrating clean spatial parameters for deep flow.”",
        tags: ["Binaural", "Minimalist", "Deep Flow"],
        bgTint: "rgba(8, 28, 24, 0.35)",
        chord: [220, 330, 440], 
        type: 'sine'
    },
    grateful: {
        voice: "“Warm resonance detected. Amplifying acoustic harmonic structural components.”",
        tags: ["Ambient", "Acoustic Warmth", "Bright Sky"],
        bgTint: "rgba(36, 28, 12, 0.35)",
        chord: [164.81, 246.94, 329.63, 392.00], 
        type: 'triangle'
    },
    tired: {
        voice: "“Low system energy. Transitioning engine to down-tempo atmospheric waves.”",
        tags: ["Lo-Fi Sleep", "Drifting", "Slow Engine"],
        bgTint: "rgba(12, 12, 16, 0.35)",
        chord: [73.42, 110, 146.83], 
        type: 'sine'
    }
};

// Global Audio Engine States
let audioCtx = null;
let activeOscillators = [];
let masterGain = null;

function initAudioEngine() {
    try {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContextClass();
        
        masterGain = audioCtx.createGain();
        masterGain.gain.setValueAtTime(0, audioCtx.currentTime); 
        masterGain.connect(audioCtx.destination);
    } catch (e) {
        console.error("Audio Context initialization failed.", e);
    }
}

function triggerDazMood(mood, element) {
    // Force wake up browser audio permissions
    if (!audioCtx) initAudioEngine();
    if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
    }

    // Visual button states
    document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('active'));
    if (element) element.classList.add('active');

    const data = moodMatrix[mood];
    if (!data) return;

    // Update dynamic text layouts
    document.getElementById('daz-voice').innerText = data.voice;
    
    const metadataEl = document.getElementById('daz-metadata');
    metadataEl.innerHTML = '';
    data.tags.forEach(tagText => {
        const span = document.createElement('span');
        span.className = 'tag';
        span.innerText = tagText;
        metadataEl.appendChild(span);
    });

    const feedbackBox = document.getElementById('daz-feedback-box');
    feedbackBox.style.backgroundColor = data.bgTint;
    feedbackBox.style.borderColor = "var(--card-color2)";

    if (!masterGain) return;

    // Crossfade: Fade out old sound nodes cleanly before spinning up the next chord
    masterGain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);

    setTimeout(() => {
        // Completely clear old running synth frequencies from memory
        killAllSoundNodes();

        // High-cut lowpass filter for a deep, cinematic cushion
        const lpFilter = audioCtx.createBiquadFilter();
        lpFilter.type = 'lowpass';
        lpFilter.frequency.setValueAtTime(260, audioCtx.currentTime); 
        lpFilter.connect(masterGain);

        // Build the synthesizer note arrays locally
        data.chord.forEach((freq, index) => {
            const osc = audioCtx.createOscillator();
            osc.type = data.type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

            const oscGain = audioCtx.createGain();
            const volumeWeight = index === 0 ? 0.35 : 0.12; 
            oscGain.gain.setValueAtTime(volumeWeight, audioCtx.currentTime);

            // Slow volume wave modulation (LFO) to create a rolling, infinite ambient soundscape
            const lfo = audioCtx.createOscillator();
            lfo.frequency.setValueAtTime(0.07 + (index * 0.03), audioCtx.currentTime);
            const lfoGain = audioCtx.createGain();
            lfoGain.gain.setValueAtTime(0.06, audioCtx.currentTime);

            lfo.connect(lfoGain);
            lfoGain.connect(oscGain.gain);
            lfo.start();

            osc.connect(oscGain);
            oscGain.connect(lpFilter);
            
            osc.start();
            activeOscillators.push(osc);
        });

        // Open master volume loop cleanly — plays forever with NO auto-timeout
        masterGain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.4); 

    }, 120);
}

// Complete hardware purge helper
function killAllSoundNodes() {
    activeOscillators.forEach(osc => {
        try { osc.stop(); osc.disconnect(); } catch(e){}
    });
    activeOscillators = [];
}

// THE MASTER KILL SWITCH
function stopAmbientStream() {
    // 1. Instantly fade the master volume down to zero
    if (masterGain) {
        masterGain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.15);
    }
    
    // 2. Tear down synth nodes from your browser's audio thread completely
    setTimeout(() => {
        killAllSoundNodes();
    }, 180);

    // 3. Clear active styling off mood buttons
    document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('active'));
    
    // 4. Reset interface panel text back to base setup
    document.getElementById('daz-voice').innerText = "Select a frequency above to awaken Daz...";
    document.getElementById('daz-metadata').innerHTML = '';
    
    const feedbackBox = document.getElementById('daz-feedback-box');
    feedbackBox.style.backgroundColor = "rgba(255, 255, 255, 0.01)";
    feedbackBox.style.borderColor = "rgba(255, 255, 255, 0.04)";
}