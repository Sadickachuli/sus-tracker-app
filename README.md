# Sus-Activity Tracker

The Sus-Activity Tracker is a web application designed to improve and expand users' knowledge of sustainable living. It serves as a supplemental enhancement to current environmental measures rather than their replacement.

![sus-tracker-signup](https://github.com/user-attachments/assets/aa4e8b0e-8d27-4101-b843-299e52ef208d)
![dashboard](https://github.com/user-attachments/assets/16682870-c701-4653-bb24-f3f438f7f12c)
![eco-tips](https://github.com/user-attachments/assets/dd980b80-c677-474f-8d32-9ecaeacef23a)
![tasks](https://github.com/user-attachments/assets/287b2196-e93e-40b3-b9b2-73bd4e95f4ce)
![convos](https://github.com/user-attachments/assets/f96eba21-32d2-4856-8b23-395166cc206e)
![profile](https://github.com/user-attachments/assets/44f40549-aedf-4b0a-9394-66b894b1b2c0)


## Features


- Provides sustainable living tips, climate news, and suggestions.
- Allows users to track their sustainable activities.
- Offers a social platform for users to share ideas, suggestions, and progress

## Technologies Used

- Flask
- SQLAlchemy
- HTML
- CSS
- JavaScript

## How to Use

To clone and run this application on your machine, follow these steps:

1. **Clone the Repository**: git clone https://github.com/Sadickachuli/sus-tracker-app.git

2. **Navigate to the Project Directory**: cd /sus-Tracker/sus-tracker-app 


3. **Install Dependencies**: pip install -r requirements.txt


4. **Set Up the Database**:
- Open a Python terminal in the project directory.
- Run the following commands:
  ```python
  from flaskapp import app, db
  app.app_context().push()
  db.create_all()
  exit()
  ```

5. **Run the Application**: in your terminal, run ***python main.py*** to start the server.


6. **Access the Application**:
Open a web browser and go to `http://localhost:5000`.

7. **Explore the Features**:
- Browse sustainable living tips and suggestions.
- Track your sustainable activities.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




