
# Medical Chatbot

## Overview

This RAG chatbot is designed to interpret handwritten medical prescriptions to enhance patient safety and healthcare efficiency. Leveraging Optical Character Recognition (OCR) technology specifically trained on medical scripts, the chatbot accurately processes prescription images, identifies medications, and retrieves detailed drug information including dosages and side effects. It aims to bridge the communication gap between healthcare providers and patients, ensuring prescriptions are understood and followed correctly.

## Key Features

- **Advanced OCR Capabilities**: Employs state-of-the-art OCR technology to decode complex handwriting on prescriptions.
- **Comprehensive Drug Database**: Accesses a secure database with detailed information on medications, including uses, side effects, and manufacturer details.
- **User-Friendly Summaries**: Converts complex prescription information into easy-to-understand summaries for patients.
- **Support for Healthcare Providers**: Provides a tool for quick verification of prescription details, enhancing patient education and safety.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.8 or later
- Django 3.1 or later
- Additional Python libraries as listed in the `requirements.txt` file

### Installation

Follow these detailed steps to get a development environment running:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/just-a-penguin/IR_projectGrp53.git
   cd IR_projectGrp53
   ```

2. Run **app.py** file to visit the website 


### Usage

Navigate to `http://127.0.0.1:8000/` in your web browser to access the user interface.

#### Example Interactions

- **Uploading a Prescription**:
  - Click on the 'Upload Prescription' button.
  - Select an image file containing a handwritten prescription.
  - View the interpreted results displayed on the screen.

- **Querying Drug Information**:
  - Use the search bar to type the name of a medication.
  - Hit enter to retrieve and display detailed information about the medication.

## Development

### Architecture

This project is built using the Django framework for the backend and a combination of HTML, CSS, and JavaScript for the frontend. The OCR functionality is powered by Keras OCR and Tesseract, integrated into our Django application as a backend service.

### Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## Team

- Aishiki Bhattacharya
- Jeremiah Malsawmkima Rokhum
- Sanskar Ranjan
- Vishal Bawa
- Saketh Ragirolla

## Acknowledgments

- Thanks to Indraprastha Institute of Information Technology Delhi (IIIT-Delhi) for their support and guidance.
- Appreciation to Tata's 1mg for providing a reliable drug database, essential for the accurate functioning of our chatbot.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## References

For more detailed information on the methodologies and technologies used, please refer to our publication and other resources linked within the repository.

## Contact

For any queries or further information, please raise an issue on the GitHub repository or contact one of the team members through their institutional email addresses.
