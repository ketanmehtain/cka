from flask import Flask, request, jsonify
import logging
logging.basicConfig(level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/tmp/debug.log"),
        logging.StreamHandler()])

pkj = Flask(__name__)


#POST route for Admission Controller
@pkj.route('/validate', methods=['POST'])

#Admission Control Logic
def deployment_webhook():
  resouce_type = ["ReplicationController", "ReplicaSet", "Deployment", "DaemonSet", "Statefulsets", "Job"]
  allowed_img = "nginx"
  
  request_info = request.get_json()
  logging.info("Request: {0}".format(request_info))
  
  uid = request_info["request"].get("uid")
  logging.info("Uid: {0}".format(uid))
  
  kind_type = request_info["request"]["kind"].get("kind")
  logging.info("Kind: {0}".format(kind_type))
  
  try:
    if kind_type in 'Pod':
      # Find the image
      pod_img = request_info["request"]["object"]["spec"]["containers"][0]["image"]
      logging.info("Pod Image: {0}".format(pod_img))
      #Check if image is allowed
      if allowed_img in pod_img:
        #Send response back to controller if validations succeeds
        return jsonify({"apiVersion": "admission.k8s.io/v1", "kind": "AdmissionReview", "response": {"allowed": True, "uid": uid, "status": {"message": "Repo exist!"}}})
      else:
        #Send response back to controller if validations failed
        return jsonify({"apiVersion": "admission.k8s.io/v1", "kind": "AdmissionReview", "response": {"allowed": False, "uid": uid, "status": {"message": "Use ocir.io registry."}}})
        
    elif kind_type in resouce_type:
      # Find the image
      dep_img = request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][0]["image"]
      logging.info("Image: {0}".format(dep_img))
      #Check if image is allowed
      if allowed_img in dep_img:
        #Send response back to controller if validations succeeds
        return jsonify({"apiVersion": "admission.k8s.io/v1", "kind": "AdmissionReview", "response": {"allowed": True, "uid": uid, "status": {"message": "Repo exist!"}}})
      else:
        #Send response back to controller if validations failed
        return jsonify({"apiVersion": "admission.k8s.io/v1", "kind": "AdmissionReview", "response": {"allowed": False, "uid": uid, "status": {"message": "Use ocir.io registry."}}})
    
    elif kind_type in "CronJob":
      #Find the image
      croj_img = request_info["request"]["object"]["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["image"]
      logging.info("Image: {0}".format(croj_img))
      #Check if image is allowed
      if allowed_img in croj_img:
        #Send response back to controller if validations succeeds
        return jsonify({"apiVersion": "admission.k8s.io/v1", "kind": "AdmissionReview", "response": {"allowed": True, "uid": uid, "status": {"message": "Repo exist!"}}})
      else:
        #Send response back to controller if validations failed
        return jsonify({"apiVersion": "admission.k8s.io/v1", "kind": "AdmissionReview", "response": {"allowed": False, "uid": uid, "status": {"message": "Use ocir.io registry."}}})
  except:
    return jsonify({"apiVersion": "admission.k8s.io/v1", "kind": "AdmissionReview", "response": {"allowed": False, "uid": uid, "status": {"message": "Use ocir.io registry."}}})

if __name__ == '__main__':
    pkj.run(ssl_context=('certs/webhook-crt.pem', 'certs/webhook-key.pem'),debug=True, host='0.0.0.0')


