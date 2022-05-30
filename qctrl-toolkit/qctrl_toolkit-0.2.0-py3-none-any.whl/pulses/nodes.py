# Copyright 2022 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""
Pulse library nodes.
"""

from typing import (
    Optional,
    Union,
)

import numpy as np
from qctrlcommons.graph import Graph
from qctrlcommons.node.node_data import (
    Pwc,
    Tensor,
)
from qctrlcommons.preconditions import check_argument

from qctrltoolkit.namespace import Namespace
from qctrltoolkit.toolkit_utils import expose


@expose(Namespace.PULSES)
def square_pulse_pwc(
    graph: Graph,
    amplitude: Union[float, Tensor],
    duration: float,
    initial_time: Optional[float] = 0,
    final_time: Optional[float] = None,
    name: Optional[str] = None,
) -> Pwc:
    r"""
    Creates a square pulse.

    The entire signal lasts from time 0 to the given duration with the
    square pulse being applied from the initial time to the final time.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    amplitude : float or Tensor
        The amplitude of the square pulse. If passed as a Tensor, it must be either a scalar or
        single-element 1D Tensor.
    duration : float
        The duration of the signal.
    initial_time : float, optional
        The start time of the square pulse. Defaults to 0.
    final_time : float, optional
        The end time of the square pulse. Must be greater than the initial time. Defaults to the
        value of the given duration.
    name : str, optional
        The name of the node.

    Returns
    -------
    Pwc
        The square pulse. The returned Pwc can have a maximum of three segments and a minimum
        of one, depending on the initial and final times of the pulse and the duration of the
        signal.

    Notes
    -----
        The square pulse is defined as

        .. math::`\mathop{\mathrm{Square}}(t) = A \theta(t-t_0) \theta(t-t_1) \; ,`

        where :math:`A` is the amplitude, :math:`t_0` is the initial time of the pulse,
        :math:`t_1` is the final time of the pulse and :math:`\theta(t)` is the Heaviside step
        function.

    Examples
    --------

    Define a square PWC pulse.

    >>> graph.pulses.square_pulse_pwc(
    ...     amplitude=2.5,
    ...     duration=4.0,
    ...     initial_time=1.0,
    ...     final_time=3.0,
    ...     name="square_pulse",
    ... )
    <Pwc: name="square_pulse", operation_name="pwc", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["square_pulse"])
    >>> result.output["square_pulse"]
    [
        {'duration': 1.0, 'value': 0.0},
        {'duration': 2.0, 'value': 2.5},
        {'duration': 1.0, 'value': 0.0}
    ]

    Define a square pulse with an optimizable amplitude.

    >>> amplitude = graph.optimization_variable(
    ...     count=1, lower_bound=0, upper_bound=2.*np.pi, name="amplitude"
    ... )
    >>> graph.pulses.square_pulse_pwc(
    ...     amplitude=amplitude, duration=4.0, name="square_pulse"
    ... )
    <Pwc: name="square_pulse", operation_name="pwc", value_shape=(), batch_shape=()>
    """

    if final_time is None:
        final_time = duration

    check_argument(
        duration > 0.0, "The duration must be positive.", {"duration": duration}
    )
    check_argument(
        final_time > initial_time,
        "The final time must be greater than the initial time.",
        {"final_time": final_time, "initial_time": initial_time},
    )

    if isinstance(amplitude, (Tensor, np.ndarray)):
        check_argument(
            amplitude.shape in [(), (1,)],
            "If passed as a Tensor, the amplitude must be either a scalar or single element 1D "
            "Tensor.",
            {"amplitude": amplitude},
            extras={"amplitude.shape": amplitude.shape},
        )

    if initial_time > duration or final_time < 0:
        # In both of these cases the signal is always zero.
        return graph.pwc(
            values=np.array([0]), durations=np.array([duration]), name=name
        )

    if initial_time > 0:
        if duration < final_time or np.isclose(duration, final_time):
            values = amplitude * np.array([0, 1])
            durations = np.array([initial_time, duration - initial_time])
        else:
            values = amplitude * np.array([0, 1, 0])
            durations = np.array(
                [initial_time, final_time - initial_time, duration - final_time]
            )
    else:
        if duration < final_time or np.isclose(duration, final_time):
            values = amplitude * np.array([1])
            durations = np.array([duration])
        else:
            values = amplitude * np.array([1, 0])
            durations = np.array([final_time, duration - final_time])

    return graph.pwc(values=values, durations=durations, name=name)
