class notifyme (
  $message = "This module just notifies a message"
) { 
  notify { $message: }
}
