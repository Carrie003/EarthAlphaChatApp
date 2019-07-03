//
//  WelcomeViewController.swift
//  Flash Chat
//
//  This is the welcome view controller - the first thign the user sees
//

import UIKit
import Firebase


class WelcomeViewController: UIViewController {

    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        //If there is a logged in user, by pass this screen and go straight to ChatViewController
        
        
        
//        if Auth.auth().currentUser != nil {
//            performSegue(withIdentifier: "goToChat", sender: self)
//        }
    
//        Auth.auth().createUser(withEmail: , password: <#T##String#>, completion: <#T##AuthDataResultCallback?##AuthDataResultCallback?##(AuthDataResult?, Error?) -> Void#>)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
}
