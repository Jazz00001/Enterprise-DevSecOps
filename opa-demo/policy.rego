package kubernetes.admission

default allow := false

privileged_container if {
  some i
  input.request.object.spec.containers[i].securityContext.privileged == true
}

allow if {
  input.request.kind.kind == "Pod"
  not privileged_container
}
