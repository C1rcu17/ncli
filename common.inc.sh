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

check_pkgs()
{
  local missing=""
  local pkg

  for pkg in "${@}"; do
    dpkg-query -s "${pkg}" 2>/dev/null | grep -q ^"Status: install ok installed"$

    if [ ${?} -ne 0 ]; then
      if [ -z "${missing}" ]; then
        missing="Missing packages:"
      fi

      missing="${missing} ${pkg}"
    fi
  done

  if [ ! -z "${missing}" ]; then
    exit_error "${missing}" 1
  fi
}
