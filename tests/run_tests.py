import unittest
from testfunctions import  Kdvv_example, Nsep_example, Nsev_example, Nsev_dstcst_variation, Nsev_inverse_example, Nsev_inverse_example2, Nsev_inverse_input_variation


kdvvsuite = unittest.TestSuite()
kdvvsuite.addTest(Kdvv_example('test_return_value'))
kdvvsuite.addTest(Kdvv_example('test_contspec'))

nsepsuite = unittest.TestSuite()
nsepsuite.addTest(Nsep_example('test_return_value'))
nsepsuite.addTest(Nsep_example('test_M_value'))
nsepsuite.addTest(Nsep_example('test_aux_spec_value'))
nsepsuite.addTest(Nsep_example('test_K_value'))
nsepsuite.addTest(Nsep_example('test_main_spec_value'))

nsevsuite1 = unittest.TestSuite()
nsevsuite1.addTest(Nsev_example('test_return_value'))
nsevsuite1.addTest(Nsev_example('test_bound_states_num_value'))
nsevsuite1.addTest(Nsev_example('test_bound_states_value'))
nsevsuite1.addTest(Nsev_example('test_disc_norm_value'))
nsevsuite1.addTest(Nsev_example('test_cont_ref_value'))

nsevsuite2 = unittest.TestSuite()
nsevsuite2.addTest(Nsev_dstcst_variation('test_dst_cst_variation'))

nsev_inverse_suite1 = unittest.TestSuite()
nsev_inverse_suite1.addTest(Nsev_inverse_example('test_return_value'))
nsev_inverse_suite1.addTest(Nsev_inverse_example('test_q_value'))
nsev_inverse_suite1.addTest(Nsev_inverse_example('test_xi_value'))


nsev_inverse_suite2 = unittest.TestSuite()
nsev_inverse_suite2.addTest(Nsev_inverse_example2('test_return_value'))
nsev_inverse_suite2.addTest(Nsev_inverse_example2('test_q_value'))

nsev_inverse_suite3 = unittest.TestSuite()
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_return_value_both'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_return_value_disc'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_return_value_cont1'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_return_value_cont2'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_return_value_cont3'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_return_value_none'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_q_value_both'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_q_value_disc'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_q_value_cont1'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_q_value_cont2'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_q_value_cont3'))
nsev_inverse_suite3.addTest(Nsev_inverse_input_variation('test_q_value_none'))


suite = unittest.TestSuite([kdvvsuite, nsepsuite,
                            nsevsuite1,nsevsuite2,
                            nsev_inverse_suite1,
                            nsev_inverse_suite2,
                            nsev_inverse_suite3])

unittest.TextTestRunner(verbosity=2).run(suite)
#unittest.TextTestRunner(verbosity=3).run(nsev_inverse_suite3)

