//
//  PostNewInfoViewController.swift
//  Flash Chat
//
//  Created by carrie shao on 7/2/19.
//  Copyright © 2019 London App Brewery. All rights reserved.
//

import UIKit
import CoreLocation

class PostNewInfoViewController: UIViewController, UITextViewDelegate, CLLocationManagerDelegate {
    
    
    
    
    @IBOutlet weak var askForJoinTextView: UITextView!
    @IBOutlet weak var startTimePicker: UIDatePicker!
    @IBOutlet weak var endTimePicker: UIDatePicker!
    @IBOutlet weak var dateText: UITextField!
    
    @IBOutlet weak var descriptionTextView: UITextView!
    
    let dateFormatter = DateFormatter()
    let initialAskForJoinText: String = "I am now at a ice cream party at 1600 grand avenue, st.paul, minnesota (5 minutes walk from my current location), come and join me!"
    let initialDescriptionText: String = "An ice cream party that for people who love all flavors of ice cream. Huge amount of chocolate mint ice cream will be served."
    let locationManager = CLLocationManager()
    var longitude: Double = 0.0
    var latitude: Double = 0.0
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        intializeDatePicker()
        initializeTimePicker()
        initalizeDescriptionText()
    
    }
    
    func initializeAskForJoinText(){
       askForJoinTextView.text = initialAskForJoinText
        askForJoinTextView.textColor = .lightGray
        askForJoinTextView.delegate = self
        
    }
  
    
    func intializeDatePicker(){
        
        startTimePicker.addTarget(self, action: #selector(addDate), for: .valueChanged)
    }
    
    func initializeTimePicker(){
       
        endTimePicker.addTarget(self, action: #selector(addDate), for: .valueChanged)
    }
    
    
    @IBAction func addDate(){
        
        dateFormatter.dateFormat = "MM/dd HH:mm"
        dateText.text = dateFormatter.string(from: startTimePicker.date)
    }
    
    @IBAction func addTime(){
        
        dateFormatter.dateFormat = "MM/dd HH:mm"
        dateText.text = dateFormatter.string(from: startTimePicker.date)
    }

    func initializeLocation(){
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.requestWhenInUseAuthorization()
        locationManager.startUpdatingLocation()
    }
    
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        let location = locations[locations.count - 1]
        if location.horizontalAccuracy > 0{
            let alert = UIAlertController(title: "", message: "Sorry, we can't get your current location", preferredStyle: .alert)
            present(alert, animated: true, completion: nil )
            locationManager.stopUpdatingLocation()
            
        }
        longitude = location.coordinate.longitude
        latitude = location.coordinate.latitude
        
        
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        //        print(error)
        let alert = UIAlertController(title: "", message: "Sorry, we can't get your current location", preferredStyle: .alert)
        present(alert, animated: true, completion: nil )
    }
    
    
    func initalizeDescriptionText(){
        descriptionTextView.text = initialDescriptionText
        descriptionTextView.textColor = .lightGray
        descriptionTextView.delegate = self
        
        
    }
    
    func textViewDidBeginEditing(_ textView: UITextView)
    {
        if(textView == askForJoinTextView && textView.text == initialAskForJoinText && textView.textColor == .lightGray){
            textView.text = ""
            textView.textColor = .black
        }
        else if(textView == descriptionTextView && textView.text == initialAskForJoinText && textView.textColor == .lightGray){
            textView.text = ""
            textView.textColor = .black
        }
        
        textView.becomeFirstResponder()
    }


    
    
    
    @IBAction func addNewInfo(_ sender: Any) {
        
        
    }
    
    
//
//    func textFieldDidBeginEditing(_ textField: UITextField)
//    {
//        if (textField.textColor == .lightGray)
//        {
//            textField.text = ""
//            textField.textColor = .black
//        }
//        textField.becomeFirstResponder()
//    }

    
}
