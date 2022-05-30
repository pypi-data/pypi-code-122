# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['slickml']

package_data = \
{'': ['*']}

install_requires = \
['bayesian-optimization>=1.2.0,<2.0.0',
 'glmnet>=2.2.1,<3.0.0',
 'hyperopt>=0.2.7,<0.3.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'shap>=0.40.0,<0.41.0',
 'xgboost>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'slickml',
    'version': '0.2.0b0',
    'description': 'SlickML: Slick Machine Learning in Python',
    'long_description': '[![build](https://github.com/slickml/slick-ml/actions/workflows/ci.yml/badge.svg)](https://github.com/slickml/slick-ml/actions/workflows/ci.yml)\n[![License](https://img.shields.io/github/license/slickml/slick-ml)](https://github.com/slickml/slick-ml/blob/master/LICENSE/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/slickml)](https://pypi.org/project/slickml/)\n![PyPI Version](https://img.shields.io/pypi/v/slickml)\n![Python Version](https://img.shields.io/pypi/pyversions/slickml)\n[![Issues](https://img.shields.io/github/issues/slickml/slick-ml)](https://github.com/slickml/slick-ml/issues)\n[![Forks](https://img.shields.io/github/forks/slickml/slick-ml)](https://github.com/slickml/slick-ml/network/members/)\n[![Stars](https://img.shields.io/github/stars/slickml/slick-ml)](https://github.com/slickml/slick-ml/stargazers/)\n\n\n<p align="center">\n<a href="https://www.slickml.com/">\n  <img src="https://raw.githubusercontent.com/slickml/slick-ml/master/assets/designs/logo_clear.png" width="250"></img></a>\n</p>\n\n<h1 align="center">\n    SlickML🧞: Slick Machine Learning in Python\n</h1>\n\n\n**SlickML** is an open-source machine learning library written in Python aimed\nat accelerating the experimentation time for a ML application. Data Scientist\ntasks can often be repetitive such as feature selection, model tuning, or\nevaluating metrics for classification and regression problems. SlickML provides\nData Scientists with a toolbox to quickly prototype solutions for a given problem with minimal code. \n\n\n## 🛠 Installation\nTo begin with, install [Python version >=3.8,<3.10](https://www.python.org) and simply run 🏃\u200d♀️ :\n```console\npip install slickml\n```\n📣  Please note that a working [Fortran Compiler](https://gcc.gnu.org/install/) (`gfortran`) is also required to build the package. If you do not have `gcc` installed, the following commands depending on your operating system will take care of this requirement.\n```console\n# Mac Users\nbrew install gcc\n\n# Linux Users\nsudo apt install build-essential       \n```\n\n### 🐍 Python Virtual Environments\nIn order to avoid any potential conflicts with other installed Python packages, it is\nrecommended to use a virtual environment, e.g. [python poetry](https://python-poetry.org/), [python virtualenv](https://docs.python.org/3/library/venv.html), [pyenv virtualenv](https://github.com/pyenv/pyenv-virtualenv), or [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). Our recommendation is to use `python-poetry` 🥰 for everything 😁.\n\n\n## 📌 Quick Start\n✅ An example to quickly run a `Feature Selection` pipeline with embedded `Cross-Validation` and `Feature-Importance` visualization: \n```python\nfrom slickml.feautre_selection import XGBoostFeatureSelector\nxfs = XGBoostFeatureSelector()\nxfs.fit(X, y)\n```\n![selection](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/feature_selection.png)\n\n```python\nxfs.plot_cv_results()\n```\n![xfscv](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/xfs_cv_results.png)\n\n```python\nxfs.plot_frequency()\n```\n![frequency](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/feature_frequency.png)\n\n✅ An example to quickly find the `tuned hyper-parameter` with `Bayesian Optimization`:\n```python\nfrom slickml.optimization import XGBoostClassifierBayesianOpt\nxbo = XGBoostClassifierBayesianOpt()\nxbo.fit(X_train, y_train)\n```\n![clfbo](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_hyper_params.png)\n\n```python\nbest_params = xbo.get_best_params()\nbest_params\n\n{"colsample_bytree": 0.8213916662259918,\n "gamma": 1.0,\n "learning_rate": 0.23148232373451072,\n "max_depth": 4,\n "min_child_weight": 5.632602921054691,\n "reg_alpha": 1.0,\n "reg_lambda": 0.39468801734425263,\n "subsample": 1.0\n }\n```\n\n✅ An example to quickly train/validate a `XGBoostCV Classifier` with `Cross-Validation`, `Feature-Importance`, and `Shap` visualizations:\n```python\nfrom slickml.classification import XGBoostCVClassifier\nclf = XGBoostCVClassifier(params=best_params)\nclf.fit(X_train, y_train)\ny_pred_proba = clf.predict_proba(X_test)\n\nclf.plot_cv_results()\n```\n![clfcv](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_cv_results.png)\n\n```python\nclf.plot_feature_importance()\n```\n![clfimp](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_feature_importance.png)\n\n```python\nclf.plot_shap_summary(plot_type="violin")\n```\n![clfshap](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_shap_summary.png)\n\n```python\nclf.plot_shap_summary(plot_type="layered_violin", layered_violin_max_num_bins=5)\n```\n![clfshaplv](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_shap_summary_lv.png)\n\n```python\nclf.plot_shap_waterfall()\n```\n![clfshapwf](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_shap_waterfall.png)\n\n\n✅ An example to train/validate a `GLMNetCV Classifier` with `Cross-Validation` and `Coefficients` visualizations:\n```python\nfrom slickml.classification import GLMNetCVClassifier\nclf = GLMNetCVClassifier(alpha=0.3, n_splits=4, metric="roc_auc")\nclf.fit(X_train, y_train)\ny_pred_proba = clf.predict_proba(X_test)\n\nclf.plot_cv_results()\n```\n![clfglmnetcv](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_glmnet_cv_results.png)\n\n```python\nclf.plot_coeff_path()\n```\n![clfglmnetpath](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_glmnet_paths.png)\n\n\n✅ An example to quickly visualize the `binary classification metrics` based on multiple `thresholds`:\n```python\nfrom slickml.metrics import BinaryClassificationMetrics\nclf_metrics = BinaryClassificationMetrics(y_test, y_pred_proba)\nclf_metrics.plot()\n```\n![clfmetrics](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/clf_metrics.png)\n\n\n✅ An example to quickly visualize some `regression metrics`:\n```python\nfrom slickml.metrics import RegressionMetrics\nreg_metrics = RegressionMetrics(y_test, y_pred)\nreg_metrics.plot()\n```\n![regmetrics](https://raw.githubusercontent.com/slickml/slick-ml/master/assets/images/reg_metrics.png)\n\n\n## 🧑\u200d💻🤝 Contributing to SlickML🧞\nYou can find the details of the development process in our [Contributing](CONTRIBUTING.md) guidelines. We strongly believe that reading and following these guidelines will help us make the contribution process easy and effective for everyone involved 🚀🌙 .\n\n\n## ❓ 🆘 📲 Need Help?\nPlease join our [Slack Channel](https://join.slack.com/t/slickml/shared_invite/zt-19taay0zn-V7R4jKNsO3n76HZM5mQfZA) to interact directly with the core team and our small community. This is a good place to discuss your questions and ideas or in general ask for help 👨\u200d👩\u200d👧 👫 👨\u200d👩\u200d👦 .\n\n\n## 📚 Citing SlickML🧞\nIf you use SlickML in an academic work 📃 🧪 🧬 , please consider citing it 🙏 .\n### Bibtex Entry:\n```bib\n@software{slickml2020,\n  title={SlickML: Slick Machine Learning in Python},\n  author={Tahmassebi, Amirhessam and Smith, Trace},\n  url={https://github.com/slickml/slick-ml},\n  version={0.2.0},\n  year={2021},\n}\n\n@article{tahmassebi2021slickml,\n  title={Slickml: Slick machine learning in python},\n  author={Tahmassebi, Amirhessam and Smith, Trace},\n  journal={URL available at: https://github. com/slickml/slick-ml},\n  year={2021}\n}\n```',
    'author': 'Amirhessam Tahmassebi',
    'author_email': 'admin@slickml.com',
    'maintainer': 'Amirhessam Tahmassebi',
    'maintainer_email': 'admin@slickml.com',
    'url': 'https://www.slickml.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
