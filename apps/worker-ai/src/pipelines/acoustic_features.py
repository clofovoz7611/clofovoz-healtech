import parselmouth
from parselmouth.praat import call
import numpy as np

def extract_vocal_biomarkers(audio_path: str) -> dict:
    """
    Procesa un archivo de audio mediante Praat / Parselmouth
    y extrae biomarcadores acústicos cuantitativos.
    """
    sound = parselmouth.Sound(audio_path)
    
    # 1. Pitch / Frecuencia Fundamental (F0)
    pitch = sound.to_pitch(time_step=0.01, pitch_floor=75.0, pitch_ceiling=600.0)
    f0_values = pitch.selected_array['frequency']
    f0_voiced = f0_values[f0_values > 0]
    
    f0_mean = float(np.mean(f0_voiced)) if len(f0_voiced) > 0 else 0.0
    f0_std = float(np.std(f0_voiced)) if len(f0_voiced) > 0 else 0.0
    
    # 2. Pulsos glóticos para cálculo de perturbación
    point_process = call(sound, "To PointProcess (periodic, cc)", 75.0, 600.0)
    
    # 3. Jitter (perturbación de frecuencia en periodos consecutivos)
    jitter_local = call(point_process, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3)
    
    # 4. Shimmer (perturbación de amplitud)
    shimmer_local = call([sound, point_process], "Get shimmer (local)", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)
    
    # 5. Harmonics-to-Noise Ratio (HNR)
    harmonicity = sound.to_harmonicity(time_step=0.01, minimum_pitch=75.0)
    hnr_values = harmonicity.values
    hnr_mean = float(np.mean(hnr_values[hnr_values != -200])) if np.any(hnr_values != -200) else 0.0

    return {
        "f0_mean_hz": round(f0_mean, 2),
        "f0_std_hz": round(f0_std, 2),
        "jitter_percent": round(jitter_local * 100, 3) if not np.isnan(jitter_local) else 0.0,
        "shimmer_percent": round(shimmer_local * 100, 3) if not np.isnan(shimmer_local) else 0.0,
        "hnr_db": round(hnr_mean, 2),
        "status": "completed"
    }