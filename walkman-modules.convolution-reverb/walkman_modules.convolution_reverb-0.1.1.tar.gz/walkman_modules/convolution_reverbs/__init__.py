from __future__ import annotations

import dataclasses
import warnings

import pyo

import walkman


class InvalidInputIndexWarning(Warning):
    pass


@dataclasses.dataclass
class ConvolutionReverb(walkman.ModuleWithDecibel):
    """"""

    impulse_path: str = ""

    def setup_pyo_object(self):
        super().setup_pyo_object()

        self._balance_signal_to = pyo.SigTo(1)
        try:
            pyo_input = self.input_provider[0]
        except IndexError:
            warnings.warn(
                f"Found no audio inputs! Using {self.get_name()} module is useless "
                "without any audio input!"
            )
            pyo_input = pyo.Sig(0)
        self._convolution_reverb = pyo.CvlVerb(
            pyo_input,
            self.impulse_path,
            mul=self._decibel_signal_to,
            bal=self._balance_signal_to,
        ).stop()

    def _play(self, duration: float = 0, delay: float = 0):
        super()._play(duration, delay)
        self._convolution_reverb.play(dur=duration, delay=delay)
        self._balance_signal_to.play(dur=duration, delay=delay)

    def _stop(self, wait: float = 0):
        super()._stop(wait)
        self._convolution_reverb.stop(wait=wait)
        self._balance_signal_to.stop(wait=wait)

    def _initialise(
        self,
        input_index: int = 0,
        decibel: walkman.Parameter = -6,  # type: ignore
        balance: walkman.Parameter = 1,  # type: ignore
    ):
        super()._initialise(decibel=decibel)

        try:
            pyo_input = self.input_provider[input_index]
        except IndexError:
            warnings.warn(
                f"There is no input with input_index = '{input_index}'!"
                f" WALKMAN ignored current cue settings for {self.get_name()}.",
                InvalidInputIndexWarning,
            )

        else:
            self._convolution_reverb.setInput(pyo_input)
            self._balance_signal_to.setValue(balance.value)

    @property
    def _pyo_object(self) -> pyo.PyoObject:
        return self._convolution_reverb
