import magenta
from magenta.models.music_vae import TrainedModel
from magenta.models.music_vae import configs
from magenta.music import midi_io
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# print(configs.CONFIG_MAP.keys())


# Load the MusicVAE configuration
config = configs.CONFIG_MAP['hierdec-trio_16bar']

# Define the trained model
vae = TrainedModel(
    config, 
    batch_size=4, 
    checkpoint_dir_or_path='/home/cluesec/Downloads/hierdec-trio_16bar.ckpt')

# Generate 4 new music sequences
samples = vae.sample(n=4)

# Save generated music as a MIDI file
midi_io.sequence_proto_to_midi_file(samples[0], 'generated_music.mid')

print("Music generated and saved as 'generated_music.mid'.")
