print_error()
{
  check_n_args ${#} 1 "print_error <error>"
  echo "${1}" >&2
}

exit_error()
{
  check_n_args ${#} 2 "exit_error <error> <code>"
  print_error "${1}"
  exit ${2}
}

check_n_args()
{
  if [ ${#} -ne 3 ]; then
    exit_error "Usage: check_n_args <argc> <nargs> <error>" 1
  fi

  if [ ${1} -ne ${2} ]; then
    exit_error "Usage: ${3}" 1
  fi
}

abs_path()
{
  check_n_args ${#} 1 "abs_path <path>"
  echo -n "$(readlink -nm "${1}")"
}

abs_dirname()
{
  check_n_args ${#} 1 "abs_dirname <path>"
  echo -n "$(dirname -z "$(abs_path "${1}")")"
}

check_cmd()
{
  check_n_args ${#} 1 "check_cmd <cmd>"

  command -v ${1} 2>&1

  if [ ${?} -ne 0 ]; then
    exit_error "Command not found: ${1}" 1
  fi
}
