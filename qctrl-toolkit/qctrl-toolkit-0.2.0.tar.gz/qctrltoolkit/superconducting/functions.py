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
Convenient functions for superconducting systems.
"""

from abc import (
    ABC,
    abstractmethod,
)
from collections import namedtuple
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

import numpy as np
from qctrlcommons.exceptions import QctrlArgumentsValueError
from qctrlcommons.graph import Graph
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_positive_integer,
)

from qctrltoolkit.namespace import Namespace
from qctrltoolkit.toolkit_utils import expose


class OptimizableCoefficient(ABC):
    """
    Abstract class for optimizable Hamiltonian coefficients.
    """

    @abstractmethod
    def get_pwc(self, graph, gate_duration, name):
        """
        Return a Pwc representation of the optimizable coefficient.
        """
        raise NotImplementedError


@expose(Namespace.SUPERCONDUCTING)
@dataclass
class RealOptimizableConstant(OptimizableCoefficient):
    """
    A real-valued optimizable constant coefficient for a Hamiltonian term.
    The main function will try to find the optimal value for this constant.

    Attributes
    ----------
    min : float
        The minimum value that the coefficient can take.
    max : float
        The maximum value that the coefficient can take.
    """

    min: float
    max: float

    def __post_init__(self):
        check_argument(
            self.min < self.max,
            "The maximum must be larger than the minimum.",
            {"min": self.min, "max": self.max},
        )

    def get_pwc(self, graph, gate_duration, name):
        value = graph.optimization_variable(1, self.min, self.max)[0]
        value.name = name
        return graph.constant_pwc(constant=value, duration=gate_duration)


@expose(Namespace.SUPERCONDUCTING)
@dataclass
class ComplexOptimizableConstant(OptimizableCoefficient):
    """
    A complex-valued optimizable constant coefficient for a Hamiltonian term.
    The main function will try to find the optimal value for this constant.

    Attributes
    ----------
    min_modulus : float
        The minimum value that the modulus of the coefficient can take.
    max_modulus : float
        The maximum value that the modulus of the coefficient can take.
    """

    min_modulus: float
    max_modulus: float

    def __post_init__(self):
        check_argument(
            self.min_modulus < self.max_modulus,
            "The maximum must be larger than the minimum.",
            {"min_modulus": self.min_modulus, "max_modulus": self.max_modulus},
        )

    def get_pwc(self, graph, gate_duration, name):
        mod = graph.optimization_variable(1, self.min_modulus, self.max_modulus)[0]
        phase = graph.optimization_variable(1, 0, 2 * np.pi, True, True)[0]
        value = graph.multiply(mod, graph.exp(1j * phase), name=name)
        return graph.constant_pwc(constant=value, duration=gate_duration)


@expose(Namespace.SUPERCONDUCTING)
@dataclass
class RealOptimizableSignal(OptimizableCoefficient):
    """
    A real-valued optimizable time-dependent piecewise-constant coefficient for
    a Hamiltonian term. The main function will try to find the optimal value for
    this signal at each segment.

    Attributes
    ----------
    count : int
        The number of segments in the piecewise-constant signal.
    min : float
        The minimum value that the signal can take at each segment.
    max : float
        The maximum value that the signal can take at each segment.
    """

    count: int
    min: float
    max: float

    def __post_init__(self):
        check_argument(
            self.count > 0, "There must be at least one segment.", {"count": self.count}
        )
        check_argument(
            self.min < self.max,
            "The maximum must be larger than the minimum.",
            {"min": self.min, "max": self.max},
        )

    def get_pwc(self, graph, gate_duration, name):
        values = graph.optimization_variable(self.count, self.min, self.max)
        return graph.pwc_signal(values=values, duration=gate_duration, name=name)


@expose(Namespace.SUPERCONDUCTING)
@dataclass
class ComplexOptimizableSignal(OptimizableCoefficient):
    """
    A complex-valued optimizable time-dependent piecewise-constant coefficient
    for a Hamiltonian term. The main function will try to find the optimal value
    for this signal at each segment.

    Attributes
    ----------
    count : int
        The number of segments in the piecewise-constant signal.
    min_modulus : float
        The minimum value that the modulus of the signal can take at each segment.
    max_modulus : float
        The maximum value that the modulus of the signal can take at each segment.
    """

    count: int
    min_modulus: float
    max_modulus: float

    def __post_init__(self):
        check_argument(
            self.count > 0, "There must be at least one segment.", {"count": self.count}
        )
        check_argument(
            self.min_modulus < self.max_modulus,
            "The maximum must be larger than the minimum.",
            {"min_modulus": self.min_modulus, "max_modulus": self.max_modulus},
        )

    def get_pwc(self, graph, gate_duration, name):
        mods = graph.optimization_variable(
            self.count, self.min_modulus, self.max_modulus
        )
        phases = graph.optimization_variable(self.count, 0, 2 * np.pi, True, True)
        return graph.pwc_signal(
            values=mods * graph.exp(1j * phases), duration=gate_duration, name=name
        )


RealCoefficient = Union[
    int, float, np.ndarray, RealOptimizableSignal, RealOptimizableConstant
]
Coefficient = Union[
    RealCoefficient, complex, ComplexOptimizableSignal, ComplexOptimizableConstant
]


def _check_argument_real_coefficient(argument, name):

    if isinstance(argument, (ComplexOptimizableSignal, ComplexOptimizableConstant)):
        check = False
    else:
        check = np.isrealobj(argument)

    check_argument(check, f"The {name} must be a real coefficient.", {name: argument})


@expose(Namespace.SUPERCONDUCTING)
@dataclass
class Transmon:
    r"""
    Class that stores all the physical system data for a transmon.

    Arguments
    ---------
    dimension : int
        Number of dimensions of the Hilbert space of the transmon.
        Must be at least 2.
    frequency : RealCoefficient, optional
        The frequency of the transmon,
        multiplying the term :math:`b^\dagger b` in the Hamiltonian.
        If not provided, it defaults to no frequency term.
    anharmonicity : RealCoefficient, optional
        The nonlinearity of the transmon,
        multiplying the term :math:`(b^\dagger)^2 b^2/2` in the Hamiltonian.
        If not provided, it defaults to no anharmonicity term.
    drive : Coefficient, optional
        The complex drive of the transmon,
        multiplying the term :math:`b^\dagger` in the Hamiltonian.
        If not provided, it defaults to no drive term.
    name : str, optional
        The identifier of the transmon that is used to link interaction terms to this transmon.
        Defaults to "transmon".

    Notes
    -----
    The Hamiltonian for the transmon is defined as

    .. math::
        H_\mathrm{transmon} =
            \omega_T b^\dagger b
            + \frac{\alpha}{2} (b^\dagger)^2 b^2
            + \frac{1}{2} \left(\gamma_T b^\dagger + H.c. \right)

    where :math:`\omega_T` is the transmon frequency,
    :math:`\alpha` is the transmon nonlinearity,
    :math:`\gamma_T` is the transmon drive,
    and :math:`H.c.` indicates the Hermitian conjugate.
    All coefficients in the Hamiltonian are optional,
    and you should only pass those relevant to your system.
    """

    dimension: int
    frequency: Optional[RealCoefficient] = None
    anharmonicity: Optional[RealCoefficient] = None
    drive: Optional[Coefficient] = None
    name: str = "transmon"

    def __post_init__(self):
        check_argument_positive_integer(self.dimension, "dimension")
        check_argument(
            self.dimension >= 2,
            "The dimension must be at least 2.",
            {"dimension": self.dimension},
        )
        _check_argument_real_coefficient(self.frequency, "frequency")
        _check_argument_real_coefficient(self.anharmonicity, "anharmonicity")


@expose(Namespace.SUPERCONDUCTING)
@dataclass
class Cavity:
    r"""
    Class that stores all the physical system data for a cavity.

    Arguments
    ---------
    dimension : int
        Number of dimensions of the Hilbert space of the cavity.
        Must be at least 2.
    frequency : RealCoefficient, optional
        The frequency of the cavity,
        multiplying the term :math:`a^\dagger a` in the Hamiltonian.
        If not provided, it defaults to no frequency term.
    kerr_coefficient: RealCoefficient, optional
        The nonlinearity of the cavity,
        multiplying the term :math:`(a^\dagger)^2 a^2/2` in the Hamiltonian.
        If not provided, it defaults to no nonlinear term.
    drive : Coefficient, optional
        The complex drive of the cavity,
        multiplying the term :math:`a^\dagger` in the Hamiltonian.
        If not provided, it defaults to no drive term.
    name : str, optional
        The identifier of the cavity that is used to link interaction terms to this cavity.
        Defaults to "cavity".

    Notes
    -----
    The Hamiltonian for the cavity is defined as

    .. math::
        H_\mathrm{cavity} =
            \omega_C a^\dagger a
            + \frac{K}{2} (a^\dagger)^2 a^2
            + \frac{1}{2} \left(\gamma_C a^\dagger + H.c. \right)

    where :math:`\omega_C` is the cavity frequency,
    :math:`K` is the Kerr coefficient,
    :math:`\gamma_C` is the cavity drive,
    and :math:`H.c.` indicates the Hermitian conjugate.
    All coefficients in the Hamiltonian are optional,
    and you should only pass those relevant to your system.
    """

    dimension: int
    frequency: Optional[RealCoefficient] = None
    kerr_coefficient: Optional[RealCoefficient] = None
    drive: Optional[Coefficient] = None
    name: str = "cavity"

    def __post_init__(self):
        check_argument_positive_integer(self.dimension, "dimension")
        check_argument(
            self.dimension >= 2,
            "The dimension must be at least 2.",
            {"dimension": self.dimension},
        )
        _check_argument_real_coefficient(self.frequency, "frequency")
        _check_argument_real_coefficient(self.kerr_coefficient, "Kerr coefficient")


@expose(Namespace.SUPERCONDUCTING)
@dataclass
class TransmonCavityInteraction:
    r"""
    Class that stores all the physical system data for the interaction
    between a transmon and a cavity.

    Arguments
    ---------
    dispersive_shift : RealCoefficient, optional
        The dispersive shift between the transmon and the cavity,
        multiplying the term :math:`a^\dagger a b^\dagger b` in the Hamiltonian.
        If not provided, it defaults to no dispersive shift term.
    rabi_coupling : Coefficient, optional
        The strength of the Rabi coupling between the transmon and the cavity,
        multiplying the term :math:`a b^\dagger` in the Hamiltonian.
        If not provided, it defaults to no Rabi coupling term.
    transmon_name: str, optional
        The name identifying the transmon in the interaction.
        Defaults to "transmon".
    cavity_name: str, optional
        The name identifying the cavity in the interaction.
        Defaults to "cavity".


    Notes
    -----
    The Hamiltonian for the interaction is defined as

    .. math::
        H_\mathrm{transmon-cavity} =
            \chi a^\dagger a b^\dagger b
            + \frac{1}{2} \left(\Omega a b^\dagger + H.c.\right)

    where :math:`\chi` is the dispersive shift,
    :math:`\Omega` is the Rabi coupling between the transmon and the cavity,
    and :math:`H.c.` indicates the Hermitian conjugate.
    All coefficients in the Hamiltonian are optional,
    and you should only pass those relevant to your system.
    """

    dispersive_shift: Optional[RealCoefficient] = None
    rabi_coupling: Optional[Coefficient] = None
    transmon_name: Optional[str] = "transmon"
    cavity_name: Optional[str] = "cavity"

    def __post_init__(self):
        _check_argument_real_coefficient(self.dispersive_shift, "dispersive shift")


@expose(Namespace.SUPERCONDUCTING)
@dataclass
class CavityCavityInteraction:
    r"""
    Class that stores all the physical system data for the interaction
    between two cavities.

    Arguments
    ---------
    cavity_names: tuple[str, str]
        The two names identifying the cavities in the interaction.
    cross_kerr_coefficient : RealCoefficient
        The cross-Kerr coefficient between the two cavities,
        multiplying the term :math:`a_1^\dagger a_1 a_2^\dagger a_2` in the Hamiltonian.
        If not provided, it defaults to no cross-Kerr term.

    Notes
    -----
    The Hamiltonian for the interaction is defined as

    .. math::
        H_\mathrm{cavity-cavity} = K_{12} a_1^\dagger a_1 a_2^\dagger a_2

    where :math:`K_{12}` is the cross-Kerr coefficient.
    """

    cavity_names: Tuple[str, str]
    cross_kerr_coefficient: RealCoefficient

    def __post_init__(self):
        check_argument(
            self.cavity_names[0] != self.cavity_names[1],
            "The names of the two cavities must be different.",
            {"cavity_names": self.cavity_names},
        )
        _check_argument_real_coefficient(
            self.cross_kerr_coefficient, "cross-Kerr coefficient"
        )


def _check_real_coefficient(obj):
    if isinstance(obj, (RealOptimizableSignal, RealOptimizableConstant)):
        return True

    if np.isscalar(obj) or isinstance(obj, np.ndarray):
        return np.isrealobj(obj)

    return False


_QHOOps = namedtuple("_QHOOps", ["a", "adag", "n"])


def _create_qho_operators(
    graph, transmons: List[Transmon], cavities: List[Cavity]
) -> Tuple[Dict[str, _QHOOps], Dict[str, _QHOOps]]:
    """
    Creates the creation, annihilation, and number operators for transmons and cavities.

    Returns a dictionary whose keys are the subsystem names and whose values are _QHOOps
    namedtuples (with field names a, adag, and n) with the operators of each subsystem.
    """

    # Dimension of the identity in the Kronecker product before and after the operator.
    pre_dim = 1
    post_dim = np.prod([system.dimension for system in transmons + cavities])

    tri_kron = lambda op1, op2, op3: graph.kron(graph.kron(op1, op2), op3)

    # Define operators for each subsystem.
    operators = {}
    for system in transmons + cavities:
        dim = system.dimension
        post_dim //= dim
        pre_eye = graph.tensor(np.eye(pre_dim))
        post_eye = graph.tensor(np.eye(post_dim))
        operators[system.name] = _QHOOps(
            tri_kron(pre_eye, graph.annihilation_operator(dim), post_eye),
            tri_kron(pre_eye, graph.creation_operator(dim), post_eye),
            tri_kron(pre_eye, graph.number_operator(dim), post_eye),
        )
        pre_dim *= dim

    return operators


def _validate_physical_system_inputs(
    transmons: List[Transmon],
    cavities: List[Cavity],
    interactions: List[Union[TransmonCavityInteraction, CavityCavityInteraction]],
) -> Tuple[List[TransmonCavityInteraction], List[CavityCavityInteraction]]:
    """
    Validates the type of the subsystems and interactions.
    Validates the subsystem names in the interactions.

    Returns two lists: the first with all the transmon-cavity interactions
    and the second with all the cavity-cavity interactions.
    """

    check_argument(
        len(transmons + cavities) > 0,
        "At least one transmon or cavity must be provided.",
        {"transmons": transmons, "cavities": cavities},
    )

    check_argument(
        all(isinstance(transmon, Transmon) for transmon in transmons),
        "Each element in transmons must be a Transmon object.",
        {"transmons": transmons},
    )
    transmon_names = [transmon.name for transmon in transmons]
    check_argument(
        len(transmon_names) == len(set(transmon_names)),
        "Transmon names must be unique.",
        {"transmons": transmons},
        extras={"[transmon.name for transmon in transmons]": transmon_names},
    )

    check_argument(
        all(isinstance(cavity, Cavity) for cavity in cavities),
        "Each element in cavities must be a Cavity object.",
        {"cavities": cavities},
    )
    cavity_names = [cavity.name for cavity in cavities]
    check_argument(
        len(cavity_names) == len(set(cavity_names)),
        "Cavity names must be unique.",
        {"cavities": cavities},
        extras={"[cavity.name for cavity in cavities]": cavity_names},
    )

    check_argument(
        len(transmon_names + cavity_names) == len(set(transmon_names + cavity_names)),
        "Transmon and cavity names must be unique.",
        {"transmons": transmons, "cavities": cavities},
        extras={
            "[transmon.name for transmon in transmons]": transmon_names,
            "[cavity.name for cavity in cavities]": cavity_names,
        },
    )

    transmon_cavity_interactions = [
        intx for intx in interactions if isinstance(intx, TransmonCavityInteraction)
    ]
    cavity_cavity_interactions = [
        intx for intx in interactions if isinstance(intx, CavityCavityInteraction)
    ]
    check_argument(
        len(transmon_cavity_interactions) + len(cavity_cavity_interactions)
        == len(interactions),
        "Each element in interactions must be a "
        "TransmonCavityInteraction or a CavityCavityInteraction object.",
        {"interactions": interactions},
    )

    tc_interaction_name_pairs = set(
        (tc_interaction.transmon_name, tc_interaction.cavity_name)
        for tc_interaction in transmon_cavity_interactions
    )
    check_argument(
        len(tc_interaction_name_pairs) == len(transmon_cavity_interactions),
        "There are duplicate transmon-cavity interaction terms.",
        {"interactions": interactions},
    )

    for tc_interaction in transmon_cavity_interactions:
        check_argument(
            tc_interaction.transmon_name in transmon_names,
            "Transmon names in transmon-cavity interaction terms "
            "must refer to transmons in the system.",
            {"transmons": transmons, "interactions": interactions},
            extras={"[transmon.name for transmon in transmons]": transmon_names},
        )
        check_argument(
            tc_interaction.cavity_name in cavity_names,
            "Cavity names in transmon-cavity interaction terms "
            "must refer to cavities in the system.",
            {"cavities": cavities, "interactions": interactions},
            extras={"[cavity.name for cavity in cavities]": cavity_names},
        )

    cc_interaction_name_pairs = set(
        frozenset(cc_interaction.cavity_names)
        for cc_interaction in cavity_cavity_interactions
    )
    check_argument(
        len(cc_interaction_name_pairs) == len(cavity_cavity_interactions),
        "There are duplicate cavity-cavity interaction terms.",
        {"interactions": interactions},
    )

    for cc_interaction in cavity_cavity_interactions:
        name_1, name_2 = cc_interaction.cavity_names
        check_argument(
            name_1 in cavity_names and name_2 in cavity_names,
            "Names in cavity-cavity interaction terms must refer to cavities in the system.",
            {"cavities": cavities, "interactions": interactions},
            extras={"[cavity.name for cavity in cavities]": cavity_names},
        )

    return transmon_cavity_interactions, cavity_cavity_interactions


def _create_superconducting_hamiltonian(
    graph: Graph,
    transmons: List[Transmon],
    cavities: List[Cavity],
    interactions: List[Union[TransmonCavityInteraction, CavityCavityInteraction]],
    gate_duration: float,
    cutoff_frequency: float,
    sample_count: int,
):
    r"""
    Creates the Hamiltonian of a system composed of a single transmon and one or more cavities.
    Returns the Hamiltonian as a Pwc node and a list with the names of the optimizable nodes
    that have been added to the graph.

    Parameters
    ----------
    graph : Graph
        The graph where the Hamiltonian will be added.
    transmons : list[Transmon]
        List of objects containing the physical information about the transmons.
    cavities : list[Cavity]
        List of objects containing the physical information about the cavities.
    interactions : list[TransmonCavityInteraction or CavityCavityInteraction]
        List of objects containing the physical information about the interactions in the system.
    gate_duration : float
        The duration of the gate.
    cutoff_frequency : float
        The cutoff frequency of a linear sinc filter to be applied to the piecewise-constant
        signals you provide for the coefficients. If None, the signals are not filtered.
    sample_count : int
        The number of segments into which the PWC terms are discretized.

    Returns
    -------
    Pwc
        A node representing the system's Hamiltonian.
    list
        The names of the graph nodes representing optimizable coefficients.
        If some of these are PWC functions and cutoff_frequency is not None,
        then the names of the filtered PWC nodes are also included.
    """

    def convert_to_pwc(coefficient: Coefficient, real_valued: bool, name: str):
        """
        Returns the Pwc representation of a coefficient.
        """

        def filter_signal(signal):
            return graph.discretize_stf(
                stf=graph.convolve_pwc(pwc=signal, kernel=kernel),
                duration=gate_duration,
                segment_count=sample_count,
                name=f"{name}_filtered",
            )

        if real_valued:
            check_argument(
                _check_real_coefficient(coefficient),
                f"{name} can't be complex.",
                {name: coefficient},
            )

        # Convert scalar value into constant Pwc.
        if np.isscalar(coefficient):
            return graph.constant_pwc(
                constant=graph.tensor(coefficient, name=name), duration=gate_duration
            )

        # Convert array into Pwc.
        if isinstance(coefficient, np.ndarray):
            signal = graph.pwc_signal(coefficient, gate_duration, name=name)

            if kernel is None:
                return signal

            return filter_signal(signal)

        # Convert Real/ComplexOptimizableConstant into optimizable constant Pwc.
        if isinstance(
            coefficient, (RealOptimizableConstant, ComplexOptimizableConstant)
        ):
            optimizable_node_names.append(name)
            return coefficient.get_pwc(graph, gate_duration, name)

        # Convert Real/ComplexOptimizableSignal into optimizable Pwc.
        if isinstance(coefficient, (RealOptimizableSignal, ComplexOptimizableSignal)):
            optimizable_node_names.append(name)
            signal = coefficient.get_pwc(graph, gate_duration, name)
            if kernel is None:
                return signal

            optimizable_node_names.append(f"{name}_filtered")
            return filter_signal(signal)

        raise QctrlArgumentsValueError(
            f"{name} has an invalid type.", {name: coefficient}
        )

    (
        transmon_cavity_interactions,
        cavity_cavity_interactions,
    ) = _validate_physical_system_inputs(transmons, cavities, interactions)

    # Define annihilation and creation operators for the transmon and the cavity.
    operators = _create_qho_operators(graph, transmons, cavities)

    # Create nested dictionary structure containing information for the different Hamiltonian terms.
    hamiltonian_info = {}

    # Add transmon terms.
    for transmon in transmons:
        transmon_ops = operators[transmon.name]
        hamiltonian_info[f"{transmon.name}.frequency"] = {
            "coefficient": transmon.frequency,
            "operator": transmon_ops.n,
            "is_hermitian": True,
        }
        hamiltonian_info[f"{transmon.name}.anharmonicity"] = {
            "coefficient": transmon.anharmonicity,
            "operator": 0.5 * (transmon_ops.n @ transmon_ops.n - transmon_ops.n),
            "is_hermitian": True,
        }
        hamiltonian_info[f"{transmon.name}.drive"] = {
            "coefficient": transmon.drive,
            "operator": transmon_ops.adag,
            "is_hermitian": False,
        }

    # Add cavity terms.
    for cavity in cavities:
        cavity_ops = operators[cavity.name]
        hamiltonian_info[f"{cavity.name}.frequency"] = {
            "coefficient": cavity.frequency,
            "operator": cavity_ops.n,
            "is_hermitian": True,
        }
        hamiltonian_info[f"{cavity.name}.kerr_coefficient"] = {
            "coefficient": cavity.kerr_coefficient,
            "operator": 0.5 * (cavity_ops.n @ cavity_ops.n - cavity_ops.n),
            "is_hermitian": True,
        }
        hamiltonian_info[f"{cavity.name}.drive"] = {
            "coefficient": cavity.drive,
            "operator": cavity_ops.adag,
            "is_hermitian": False,
        }

    # Add transmon-cavity interaction terms.
    for tc_interaction in transmon_cavity_interactions:
        transmon_ops = operators[tc_interaction.transmon_name]
        cavity_ops = operators[tc_interaction.cavity_name]
        key = f"{tc_interaction.transmon_name}_{tc_interaction.cavity_name}_interaction"
        hamiltonian_info[f"{key}.dispersive_shift"] = {
            "coefficient": tc_interaction.dispersive_shift,
            "operator": transmon_ops.n @ cavity_ops.n,
            "is_hermitian": True,
        }
        hamiltonian_info[f"{key}.rabi_coupling"] = {
            "coefficient": tc_interaction.rabi_coupling,
            "operator": transmon_ops.adag @ cavity_ops.a,
            "is_hermitian": False,
        }

    # Add cavity-cavity interaction terms.
    for cc_interaction in cavity_cavity_interactions:
        name_1, name_2 = cc_interaction.cavity_names
        cavity_1_ops = operators[name_1]
        cavity_2_ops = operators[name_2]
        key = f"{name_1}_{name_2}_interaction"
        hamiltonian_info[f"{key}.cross_kerr_coefficient"] = {
            "coefficient": cc_interaction.cross_kerr_coefficient,
            "operator": cavity_1_ops.n @ cavity_2_ops.n,
            "is_hermitian": True,
        }

    check_argument(
        any(info["coefficient"] for info in hamiltonian_info.values()),
        "The system must contain at least one Hamiltonian coefficient.",
        {"transmons": transmons, "cavities": cavities, "interactions": interactions},
    )

    # Create kernel to filter signals (used in convert_to_pwc).
    if cutoff_frequency is not None:
        kernel = graph.sinc_convolution_kernel(cutoff_frequency)
    else:
        kernel = None

    # Build the Hamiltonian from the different terms.
    hamiltonian_terms = []
    optimizable_node_names = []  # filled up by convert_to_pwc

    for name, info in hamiltonian_info.items():
        if info["coefficient"] is not None:
            coefficient = convert_to_pwc(
                coefficient=info["coefficient"],
                real_valued=info["is_hermitian"],
                name=name,
            )
            if info["is_hermitian"]:
                hamiltonian_terms.append(coefficient * info["operator"])
            else:
                hamiltonian_terms.append(0.5 * coefficient * info["operator"])
                hamiltonian_terms.append(
                    0.5 * graph.conjugate(coefficient) * graph.adjoint(info["operator"])
                )

    return graph.pwc_sum(hamiltonian_terms), optimizable_node_names


def _extract_output(item):
    """
    Converts a non-batched item from a qctrl.types.graph/optimization.Result.output
    dictionary into a NumPy array.

    If the item is a dictionary (corresponds to a tensor), then its "value" is returned.

    If the item is a list of dictionaries (corresponds to a Pwc), then the "value"
    elements of its inner dictionaries are returned in a NumPy array.
    """
    if isinstance(item, dict):
        return item["value"]
    if isinstance(item, list):
        assert all(
            isinstance(elem, dict) for elem in item
        ), "Batches are not supported."
        return np.array([seg["value"] for seg in item])
    assert False, "Unknown output format."


@expose(Namespace.SUPERCONDUCTING)
def simulate(
    qctrl: Any,
    transmons: List[Transmon],
    cavities: List[Cavity],
    interactions: List[Union[TransmonCavityInteraction, CavityCavityInteraction]],
    gate_duration: float,
    sample_count: int = 128,
    cutoff_frequency: Optional[float] = None,
    initial_state: Optional[np.ndarray] = None,
):
    r"""
    Simulates a system composed of transmons and cavities.

    Parameters
    ----------
    qctrl : qctrl.Qctrl
        Boulder Opal session object.
    transmons : list[Transmon]
        List of objects containing the physical information about the transmons.
        It must not contain any optimizable coefficients.
        It can be an empty list, but at least one transmon or cavity must be provided.
    cavities : list[Cavity]
        List of objects containing the physical information about the cavities.
        They must not contain any optimizable coefficients.
        It can be an empty list, but at least one transmon or cavity must be provided.
    interactions : list[TransmonCavityInteraction or CavityCavityInteraction]
        List of objects containing the physical information about the interactions in the system.
        They must not contain any optimizable coefficients.
        It can be an empty list.
    gate_duration : float
        The duration of the gate to be simulated, :math:`t_\mathrm{gate}`.
        It must be greater than zero.
    sample_count : int, optional
        The number of times between 0 and `gate_duration` (included)
        at which the evolution is sampled.
        Defaults to 128.
    cutoff_frequency : float, optional
        The cutoff frequency of a linear sinc filter to be applied to the piecewise-constant
        signals you provide for the coefficients. If not provided, the signals are not filtered.
        If the signals are filtered, a larger sample count leads to a more accurate numerical
        integration. (If the signals are not filtered, the sample count has no effect on the
        numerical precision of the integration.)
    initial_state : np.ndarray, optional
        The initial state of the system, :math:`|\Psi_\mathrm{initial}\rangle`, as a 1D array of
        length ``D = np.prod([system.dimension for system in transmons + cavities])``.
        If not provided, the function only returns the system's unitary time-evolution operators.

    Returns
    -------
    dict
        A dictionary containing information about the time evolution of the system, with keys

            ``sample_times``
                The times at which the system's evolution is sampled,
                as an array of shape ``(T,)``.
            ``unitaries``
                The system's unitary time-evolution operators at each sample time,
                as an array of shape ``(T, D, D)``.
            ``state_evolution``
                The time evolution of the initial state at each sample time,
                as an array of shape ``(T, D)``.
                This is only returned if you provide an initial state.

    Notes
    -----
    The Hamiltonian of the system is of the form

    .. math::
        H = \sum_i H_{\mathrm{transmon}_i}
            + \sum_i H_{\mathrm{cavity}_i}
            + \sum_{i,j} H_{\mathrm{transmon}_i-\mathrm{cavity}_j}
            + \sum_{i,j} H_{\mathrm{cavity}_i-\mathrm{cavity}_j}

    where i and j mark the i-th and j-th transmon or cavity.
    For their definition of each Hamiltonian term, see its respective class.

    The Hilbert space of the system is defined as the outer product of all the
    transmon Hilbert spaces (in the order they're provided in `transmons`) with
    the cavity Hilbert spaces (in the order they're provided in `cavities`), that is:

    .. math::
        \mathcal{H} =
            \mathcal{H}_{\mathrm{transmon}_1} \otimes \mathcal{H}_{\mathrm{transmon}_2}
            \otimes \ldots
            \otimes \mathcal{H}_{\mathrm{cavity}_1} \otimes \mathcal{H}_{\mathrm{cavity}_2}
            \otimes \ldots

    The system dimension `D` is then the product of all transmon and cavity dimensions.
    """

    system_dimension = np.prod(
        [system.dimension for system in transmons + cavities], dtype=int
    )

    if initial_state is not None:
        check_argument(
            initial_state.shape == (system_dimension,),
            "Initial state must be a 1D array of length "
            "np.prod([system.dimension for system in transmons + cavities]).",
            {
                "initial_state": initial_state,
                "transmons": transmons,
                "cavities": cavities,
            },
            extras={
                "initial_state.shape": initial_state.shape,
                "np.prod([system.dimension for system in transmons + cavities])": system_dimension,
            },
        )
    check_argument(
        gate_duration > 0,
        "The gate duration must be greater than zero.",
        {"gate_duration": gate_duration},
    )

    # Create graph object.
    graph = qctrl.create_graph()

    # Create PWC Hamiltonian.
    hamiltonian, optimizable_node_names = _create_superconducting_hamiltonian(
        graph=graph,
        transmons=transmons,
        cavities=cavities,
        interactions=interactions,
        gate_duration=gate_duration,
        cutoff_frequency=cutoff_frequency,
        sample_count=sample_count,
    )

    # Check whether there are any optimizable coefficients.
    check_argument(
        len(optimizable_node_names) == 0,
        "None of the Hamiltonian terms can be optimizable.",
        {"transmons": transmons, "cavities": cavities, "interactions": interactions},
    )

    # Calculate the evolution.
    sample_times = np.linspace(
        gate_duration / sample_count, gate_duration, sample_count
    )
    unitaries = graph.time_evolution_operators_pwc(
        hamiltonian=hamiltonian, sample_times=sample_times, name="unitaries"
    )
    output_node_names = ["unitaries"]

    if initial_state is not None:
        states = unitaries @ initial_state[:, None]
        states = states[..., 0]
        states.name = "state_evolution"
        output_node_names.append("state_evolution")

    simulation_result = qctrl.functions.calculate_graph(
        graph=graph, output_node_names=output_node_names
    )

    # Retrieve results and build output dictionary.
    result_dict = {"sample_times": sample_times}

    for key in output_node_names:
        result_dict[key] = _extract_output(simulation_result.output[key])

    return result_dict


@expose(Namespace.SUPERCONDUCTING)
def optimize(
    qctrl: Any,
    transmons: List[Transmon],
    cavities: List[Cavity],
    interactions: List[Union[TransmonCavityInteraction, CavityCavityInteraction]],
    gate_duration: float,
    initial_state: Optional[np.ndarray] = None,
    target_state: Optional[np.ndarray] = None,
    target_operation: Optional[np.ndarray] = None,
    sample_count: int = 128,
    cutoff_frequency: Optional[float] = None,
    target_cost: Optional[float] = None,
    optimization_count: int = 5,
):
    r"""
    Finds optimal pulses or parameters for a system composed of transmons and cavities,
    in order to achieve a target state or implement a target operation.

    At least one of the terms in the transmon, cavities, or interaction Hamiltonians
    must be optimizable.

    To optimize a state transfer, you need to provide an initial and a target state.
    To optimize a target gate/unitary, you need to provide a target operation.

    Parameters
    ----------
    qctrl : qctrl.Qctrl
        Boulder Opal session object.
    transmons : list[Transmon]
        List of objects containing the physical information about the transmons.
        It can be an empty list, but at least one transmon or cavity must be provided.
    cavities : list[Cavity]
        List of objects containing the physical information about the cavities.
        It can be an empty list, but at least one transmon or cavity must be provided.
    interactions : list[TransmonCavityInteraction or CavityCavityInteraction]
        List of objects containing the physical information about the interactions in the system.
        It can be an empty list.
    gate_duration : float
        The duration of the gate to be optimized, :math:`t_\mathrm{gate}`.
        It must be greater than zero.
    initial_state : np.ndarray, optional
        The initial state of the system, :math:`|\Psi_\mathrm{initial}\rangle`, as a 1D array of
        length ``D = np.prod([system.dimension for system in transmon + cavities])``.
        If provided, the function also returns its time evolution.
        This is a required parameter if you pass a `target_state`.
    target_state : np.ndarray, optional
        The target state of the optimization, :math:`|\Psi_\mathrm{target}\rangle`,
        as a 1D array of length `D`.
        You must provide exactly one of `target_state` or `target_operation`.
    target_operation : np.ndarray, optional
        The target operation of the optimization, :math:`U_\mathrm{target}`,
        as a 2D array of shape ``(D, D)``.
        You must provide exactly one of `target_state` or `target_operation`.
    sample_count : int, optional
        The number of times between 0 and `gate_duration` (included)
        at which the evolution is sampled.
        Defaults to 128.
    cutoff_frequency: float, optional
        The cutoff frequency of a linear sinc filter to be applied to the piecewise-constant
        signals you provide for the coefficients. If not provided, the signals are not filtered.
        If the signals are filtered, a larger sample count leads to a more accurate numerical
        integration. (If the signals are not filtered, the sample count has no effect on the
        numerical precision of the integration.)
    target_cost : float, optional
        A target value of the cost that you can set as an early stop condition for the optimizer.
        If not provided, the optimizer runs until it converges.
    optimization_count : int, optional
        The number of independent randomly seeded optimizations to perform. The result
        from the best optimization (the one with the lowest cost) is returned.
        Defaults to 5.

    Returns
    -------
    dict
        A dictionary containing the optimized coefficients and information about the time evolution
        of the system, with keys

            ``optimized_values``
                Dictionary with keys such as ``transmon.drive``, ``[cavity_name].frequency``,
                ``[transmon_name]_[cavity_name]_interaction.dispersive_shift``, and
                ``[cavity_1_name]_[cavity_2_name]_interaction.cross_kerr_coefficient`` (where
                ``[transmon_n_name]`` and  ``[cavity_n_name]`` are the names assigned to the
                transmons or cavities in the interactions);
                and whose values are the requested optimized Hamiltonian coefficients.
                The values are float/complex for constant coefficients and np.ndarray for
                piecewise-constant signals. If you pass a `cutoff_frequency`, the filtered
                versions of the piecewise-constant coefficients are also included with keys
                such as ``transmon.drive_filtered``.
            ``infidelity``
                The state/operational infidelity of the optimized evolution.
            ``sample_times``
                The times at which the system's evolution is sampled,
                as an array of shape ``(T,)``.
            ``unitaries``
                The system's unitary time-evolution operators at each sample time,
                as an array of shape ``(T, D, D)``.
            ``state_evolution``
                The time evolution of the initial state at each sample time,
                as an array of shape ``(T, D)``.
                This is only returned if you provide an initial state.

    Notes
    -----
    The Hamiltonian of the system is of the form

    .. math::
        H = \sum_i H_{\mathrm{transmon}_i}
            + \sum_i H_{\mathrm{cavity}_i}
            + \sum_{i,j} H_{\mathrm{transmon}_i-\mathrm{cavity}_j}
            + \sum_{i,j} H_{\mathrm{cavity}_i-\mathrm{cavity}_j}

    where i and j mark the i-th and j-th transmon or cavity.
    For their definition of each Hamiltonian term, see its respective class.

    The Hilbert space of the system is defined as the outer product of all the
    transmon Hilbert spaces (in the order they're provided in `transmons`) with
    the cavity Hilbert spaces (in the order they're provided in `cavities`), that is:

    .. math::
        \mathcal{H} =
            \mathcal{H}_{\mathrm{transmon}_1} \otimes \mathcal{H}_{\mathrm{transmon}_2}
            \otimes \ldots
            \otimes \mathcal{H}_{\mathrm{cavity}_1} \otimes \mathcal{H}_{\mathrm{cavity}_2}
            \otimes \ldots

    The system dimension `D` is then the product of all transmon and cavity dimensions.

    If you provide an `initial_state` and a `target_state`, the optimization cost is defined as the
    infidelity of the state transfer process,

    .. math::
        \mathcal{I}
            = 1 - \left|
                \langle \Psi_\mathrm{target} | U(t_\mathrm{gate}) | \Psi_\mathrm{initial} \rangle
            \right|^2 ,

    where :math:`U(t)` is the unitary time-evolution operator generated by the Hamiltonian.

    If you provide a `target_operation`, the optimization cost is defined as the operational
    infidelity,

    .. math::
        \mathcal{I}
            = 1 - \left| \frac
                {\mathrm{Tr} (U_\mathrm{target}^\dagger U(t_\mathrm{gate}))}
                {\mathrm{Tr} (U_\mathrm{target}^\dagger U_\mathrm{target})}
            \right|^2 .
    """

    check_argument(
        (target_state is None) ^ (target_operation is None),
        "You have to provide exactly one of `target_state` or `target_operation`.",
        {"target_state": target_state, "target_operation": target_operation},
    )

    system_dimension = np.prod(
        [system.dimension for system in transmons + cavities], dtype=int
    )

    if initial_state is not None:
        check_argument(
            initial_state.shape == (system_dimension,),
            "Initial state must be a 1D array of length "
            "np.prod([system.dimension for system in transmons + cavities]).",
            {
                "initial_state": initial_state,
                "transmons": transmons,
                "cavities": cavities,
            },
            extras={
                "initial_state.shape": initial_state.shape,
                "np.prod([system.dimension for system in transmons + cavities])": system_dimension,
            },
        )

    if target_state is not None:
        check_argument(
            initial_state is not None,
            "If you provide a `target_state`, you must provide an `initial_state`.",
            {"target_state": target_state, "initial_state": initial_state},
        )
        check_argument(
            target_state.shape == (system_dimension,),
            "Target state must be a 1D array of length "
            "np.prod([system.dimension for system in transmons + cavities]).",
            {
                "target_state": target_state,
                "transmons": transmons,
                "cavities": cavities,
            },
            extras={
                "target_state.shape": target_state.shape,
                "np.prod([system.dimension for system in transmons + cavities])": system_dimension,
            },
        )

    if target_operation is not None:
        check_argument(
            target_operation.shape == (system_dimension, system_dimension),
            "Target operation must be a square operator of shape (D, D) with "
            "D = np.prod([system.dimension for system in transmons + cavities]).",
            {
                "target_operation": target_operation,
                "transmons": transmons,
                "cavities": cavities,
            },
            extras={"target_operation.shape": target_operation.shape},
        )

    check_argument(
        gate_duration > 0,
        "The gate duration must be grater than zero.",
        {"gate_duration": gate_duration},
    )

    # Create graph object.
    graph = qctrl.create_graph()

    # Create PWC Hamiltonian.
    hamiltonian, optimizable_node_names = _create_superconducting_hamiltonian(
        graph=graph,
        transmons=transmons,
        cavities=cavities,
        interactions=interactions,
        gate_duration=gate_duration,
        cutoff_frequency=cutoff_frequency,
        sample_count=sample_count,
    )

    # Check whether there are any optimizable coefficients.
    check_argument(
        len(optimizable_node_names) > 0,
        "At least one of the Hamiltonian terms must be optimizable.",
        {"transmons": transmons, "cavities": cavities, "interactions": interactions},
    )

    other_output_node_names = ["unitaries", "infidelity"]

    # Calculate the evolution.
    sample_times = np.linspace(
        gate_duration / sample_count, gate_duration, sample_count
    )
    unitaries = graph.time_evolution_operators_pwc(
        hamiltonian=hamiltonian, sample_times=sample_times, name="unitaries"
    )

    if initial_state is not None:
        states = unitaries @ initial_state[:, None]
        states = states[..., 0]
        states.name = "state_evolution"
        other_output_node_names.append("state_evolution")

    # Calculate the infidelity.
    if target_state is not None:
        graph.state_infidelity(target_state, states[-1], name="infidelity")
    else:
        graph.unitary_infidelity(unitaries[-1], target_operation, name="infidelity")

    # Execute optimization.
    optimization_result = qctrl.functions.calculate_optimization(
        graph=graph,
        cost_node_name="infidelity",
        output_node_names=optimizable_node_names + other_output_node_names,
        target_cost=target_cost,
        optimization_count=optimization_count,
    )

    # Retrieve results and build output dictionary.
    result_dict = {"optimized_values": {}, "sample_times": sample_times}

    for key in optimizable_node_names:
        result_dict["optimized_values"][key] = _extract_output(
            optimization_result.output[key]
        )

    for key in other_output_node_names:
        result_dict[key] = _extract_output(optimization_result.output[key])

    return result_dict
