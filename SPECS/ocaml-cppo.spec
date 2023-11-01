%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if !%{opt}
%global debug_package %{nil}
%endif

Name:           ocaml-cppo
Version:        1.6.4
Release:        4%{?dist}
Summary:        Equivalent of the C preprocessor for OCaml programs

License:        BSD
URL:            http://mjambon.com/cppo.html
Source0:        https://github.com/mjambon/cppo/archive/v%{version}.tar.gz

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib
%if !%{opt}
Requires:       ocaml >= 3.10.0
%endif
BuildRequires:  ocaml-ocamlbuild-devel
#BuildRequires:  jbuilder

%define libname %(sed -e 's/^ocaml-//' <<< %{name})

%description
Cppo is an equivalent of the C preprocessor targeted at the OCaml
language and its variants.

The main purpose of cppo is to provide a lightweight tool for simple
macro substitution (＃define) and file inclusion (＃include) for the
occasional case when this is useful in OCaml. Processing specific
sections of files by calling external programs is also possible via
＃ext directives.

The implementation of cppo relies on the standard library of OCaml and
on the standard parsing tools Ocamllex and Ocamlyacc, which contribute
to the robustness of cppo across OCaml versions.


%prep
%setup -q -n %{libname}-%{version}


%build
# As we don't have jbuild on RHEL, just build the sources by hand.
pushd src
ocamllex cppo_lexer.mll
ocamlyacc cppo_parser.mly
echo 'let cppo_version = "v%{version}"' > cppo_version.ml
ocamlfind opt -g -package str,unix cppo_version.mli cppo_version.ml cppo_types.mli cppo_types.ml cppo_parser.mli cppo_parser.ml cppo_lexer.ml cppo_command.mli cppo_command.ml cppo_eval.mli cppo_eval.ml cppo_main.ml -linkpkg -o cppo
popd

%install
%{__install} -d $RPM_BUILD_ROOT%{_bindir}
%{__install} -p src/cppo $RPM_BUILD_ROOT%{_bindir}/


#%check
#%ifnarch %{arm} %{power64}
## Fails on armv7hl and ppc64le with:
## Error: math error
#make test
#%endif


%files
%license LICENSE.md
%doc Changes README.md
%{_bindir}/cppo


%changelog
* Mon Jul 16 2018 Richard W.M. Jones <rjones@redhat.com> - 1.6.4-4
- RHEL 8: Remove jbuilder dependency.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.6.4-2
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.6.4-1
- New upstream version 1.6.4.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-8
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-6
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-5
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-2
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-1
- New upstream version 1.5.0 (for OCaml 4.04.1).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-1
- New upstream version 1.4.0.
- Fix download source URL.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-2
- OCaml 4.02.3 rebuild.

* Fri Jul 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- New upstream release 1.1.2.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-4
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-3
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-2
- ocaml-4.02.1 rebuild.

* Mon Nov  3 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-9
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-8
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-6
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 28 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-5
- Rebuild for OCaml 4.02.0 beta.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jaromir Capik <jcapik@redhat.com> - 0.9.3-3
- Removing ExclusiveArch

* Mon Jan 27 2014 Michel Salim <salimma@fedoraproject.org> - 0.9.3-2
- Incorporate review feedback

* Mon Jan 20 2014 Michel Salim <salimma@fedoraproject.org> - 0.9.3-1
- Initial package
