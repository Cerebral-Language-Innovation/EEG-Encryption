
from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs,corrmap)
from mne import Epochs, pick_types, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

tmin, tmax = -1., 4.
event_id = dict(hands=2, feet=3)
subject = 1



run1=[3,4,6]#Open left hand, Open right hand, Move both feet
run2=[5,6,4]#Imagine moving both hands, Imagine moving both feet, Imagine moving right hand
run3=[8,11,14]#Open right hand, Imagine moving left hand, Imagine moving both feet
run4=[10,12,7]#Open both hands, Open left hand, Open right hand
runs = run3 # chooses movements

raw_fnames = eegbci.load_data(subject, runs)
raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
eegbci.standardize(raw)
montage = make_standard_montage('standard_1005')
raw.set_montage(montage)
raw.rename_channels(lambda x: x.strip('.'))

raw.crop(tmax=60.)
raw.filter(27., 30.)

picks = pick_types(raw.info, eeg=True)

ica = ICA(n_components=32, random_state=97)
ica.fit(raw)

raw.load_data()

ica.plot_sources(raw, show_scrollbars=False)
#ica.plot_properties(raw, picks=[0, 1])
icaArray = ica.get_components()
print(icaArray)
#sIcaArray = base64.b64encode(icaArray)
bIcaArray = icaArray.tobytes()
ica.plot_components()

def dKey(arrayInBytes):
  salt = os.urandom(16)
  # derive
  kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt,
      iterations=100000,
  )
  key = kdf.derive(arrayInBytes)
  # verify
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
  )
  kdf.verify(arrayInBytes, key)
  return key

key = dKey(bIcaArray)
print(key)