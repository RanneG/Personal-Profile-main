<?php

$errors = [];

if (!empty($_POST)) {
   $name = $_POST['name'];
   $email = $_POST['email'];
   $message = $_POST['message'];
  
   if (empty($name)) {
       $errors[] = 'Name is empty';
   }

   if (empty($email)) {
       $errors[] = 'Email is empty';
   } else if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
       $errors[] = 'Email is invalid';
   }

   if (empty($message)) {
       $errors[] = 'Message is empty';
   }
}

if (!empty($errors)) {
   $allErrors = join('<br/>', $errors);
   $errorMessage = "<p style='color: red;'>{$allErrors}</p>";
}

?>